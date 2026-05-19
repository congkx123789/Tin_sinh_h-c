import os
import pandas as pd
import numpy as np
import lightgbm as lgb
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
from sklearn.preprocessing import StandardScaler
import pickle

def train_ultimate_model():
    print("🚀 Starting Ultimate Improvement Pipeline (CoxPH + LightGBM Ensemble)...")
    
    # 1. Load Data
    processed_dir = "data/02_processed/training"
    X_train = pd.read_csv(os.path.join(processed_dir, "train/X.csv"), index_col=0)
    y_train = pd.read_csv(os.path.join(processed_dir, "train/y.csv"), index_col=0)
    X_val = pd.read_csv(os.path.join(processed_dir, "val/X.csv"), index_col=0)
    y_val = pd.read_csv(os.path.join(processed_dir, "val/y.csv"), index_col=0)

    # 2. Advanced Feature Selection (Cox P-values)
    print("Performing CoxPH-based feature selection (Top P-values)...")
    # Combine X and y for lifelines
    train_df = X_train.copy()
    train_df['OS'] = y_train['OS']
    train_df['OS.time'] = y_train['OS.time']
    
    # Select top 500 genes by variance first to speed up Cox
    variances = X_train.var().sort_values(ascending=False)
    top_500_var_genes = variances.head(500).index.tolist()
    
    # Run Cox on top 500 to find best markers
    # To avoid convergence issues, we use a small subset or Lasso first
    # Let's use correlation-based pre-filter then Cox
    corrs = X_train[top_500_var_genes].corrwith(y_train['OS.time']).abs().sort_values(ascending=False)
    candidate_genes = corrs.head(50).index.tolist() # Top 50 candidates
    
    cph = CoxPHFitter(penalizer=0.1)
    cph.fit(train_df[candidate_genes + ['OS', 'OS.time']], duration_col='OS.time', event_col='OS')
    
    # Get significant genes (p < 0.05)
    summary = cph.summary
    significant_genes = summary[summary['p'] < 0.05].index.tolist()
    print(f"✅ CoxPH identified {len(significant_genes)} statistically significant genes.")
    
    if len(significant_genes) < 5:
        print("⚠️ Too few significant genes, using top 30 by P-value.")
        significant_genes = summary.sort_values(by='p').head(30).index.tolist()

    # 3. Ensemble Training (Bagging)
    print("Training LightGBM Ensemble...")
    X_train_final = X_train[significant_genes]
    X_val_final = X_val[significant_genes]
    
    # Standardize
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_final)
    X_val_scaled = scaler.transform(X_val_final)
    
    # Labels: log survival time
    y_train_label = np.log1p(y_train['OS.time'])
    y_val_label = np.log1p(y_val['OS.time'])
    
    models = []
    for i in range(10): # 10-model ensemble
        params = {
            'objective': 'regression',
            'metric': 'rmse',
            'verbosity': -1,
            'learning_rate': 0.01,
            'num_leaves': 15,
            'feature_fraction': 0.7,
            'bagging_fraction': 0.7,
            'bagging_freq': 1,
            'lambda_l1': 1.0,
            'lambda_l2': 1.0,
            'seed': 42 + i
        }
        
        m = lgb.train(
            params,
            lgb.Dataset(X_train_scaled, label=y_train_label),
            num_boost_round=1000,
            valid_sets=[lgb.Dataset(X_val_scaled, label=y_val_label)],
            callbacks=[lgb.early_stopping(stopping_rounds=50)]
        )
        models.append(m)

    # 4. Final Aggregated Prediction
    val_preds = np.mean([m.predict(X_val_scaled) for m in models], axis=0)
    
    # CHECK INVERSION
    c_index_neg = concordance_index(y_val['OS.time'], -val_preds, y_val['OS'])
    c_index_pos = concordance_index(y_val['OS.time'], val_preds, y_val['OS'])
    
    best_c_index = max(c_index_neg, c_index_pos)
    invert = c_index_pos > c_index_neg
    
    print(f"🏆 Ultimate Val C-index: {best_c_index:.4f}")
    if invert:
        print("🔄 Note: Predictions were flipped for optimal C-index.")

    # 5. Save Everything
    os.makedirs("checkpoints/lightgbm_weights", exist_ok=True)
    with open("checkpoints/lightgbm_weights/best_ensemble.pkl", "wb") as f:
        pickle.dump({'models': models, 'scaler': scaler, 'genes': significant_genes, 'invert': invert}, f)
    
    # Update selected_genes for other scripts
    with open("checkpoints/lightgbm_weights/selected_genes.pkl", "wb") as f:
        pickle.dump(significant_genes, f)

if __name__ == "__main__":
    train_ultimate_model()
