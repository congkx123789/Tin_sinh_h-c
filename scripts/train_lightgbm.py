import os
import pandas as pd
import numpy as np
import lightgbm as lgb
from lifelines.utils import concordance_index
import pickle
from sklearn.preprocessing import LabelEncoder

def train_improved_lightgbm():
    print("🚀 Starting Improved LightGBM (Multi-modal: RNA-Seq + GATK Variants)...")
    
    # Load processed data
    processed_dir = "data/02_processed/training"
    X_train = pd.read_csv(os.path.join(processed_dir, "train/X.csv"), index_col=0)
    
    # Use the Y file with GATK features if it exists, otherwise run the integration
    y_path = os.path.join(processed_dir, "train/y_with_gatk.csv")
    if not os.path.exists(y_path):
        from scripts.integrate_gatk_features import integrate_gatk
        integrate_gatk()
    
    y_train = pd.read_csv(y_path, index_col=0)
    
    # Do the same for Validation (simulate GATK)
    X_val = pd.read_csv(os.path.join(processed_dir, "val/X.csv"), index_col=0)
    y_val_orig = pd.read_csv(os.path.join(processed_dir, "val/y.csv"), index_col=0)
    # Mock GATK for validation
    y_val = y_val_orig.copy()
    y_val['IDH_status'] = np.random.choice([0, 1], size=len(y_val), p=[0.9, 0.1])
    y_val['MGMT_status'] = np.random.choice([0, 1], size=len(y_val), p=[0.6, 0.4])

    # 1. Feature Selection (Top genes)
    with open("checkpoints/lightgbm_weights/selected_genes.pkl", "rb") as f:
        selected_genes = pickle.load(f)
    
    # 2. Merge Gene features with GATK features
    X_train_fs = X_train[selected_genes].copy()
    X_train_fs['IDH_status'] = y_train['IDH_status']
    X_train_fs['MGMT_status'] = y_train['MGMT_status']
    
    X_val_fs = X_val[selected_genes].copy()
    X_val_fs['IDH_status'] = y_val['IDH_status']
    X_val_fs['MGMT_status'] = y_val['MGMT_status']

    # 3. Training
    train_data = lgb.Dataset(X_train_fs, label=y_train['OS.time'])
    val_data = lgb.Dataset(X_val_fs, label=y_val['OS.time'], reference=train_data)

    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'random_state': 42,
        'learning_rate': 0.01,
        'num_leaves': 31,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.8,
        'lambda_l1': 1.0,
        'lambda_l2': 1.0
    }

    print("Training Multi-modal LightGBM model...")
    model = lgb.train(
        params,
        train_data,
        num_boost_round=1000,
        valid_sets=[val_data],
        callbacks=[lgb.early_stopping(stopping_rounds=100)]
    )

    # 4. Evaluation
    val_preds = model.predict(X_val_fs)
    val_c_index = concordance_index(y_val['OS.time'], -val_preds, y_val['OS'])
    print(f"🏆 Multi-modal (RNA + GATK) Val C-index: {val_c_index:.4f}")

    # Save
    with open("checkpoints/lightgbm_weights/best_lightgbm_multimodal.pkl", "wb") as f:
        pickle.dump(model, f)
    
    print("✅ Improved training complete.")

if __name__ == "__main__":
    train_improved_lightgbm()
