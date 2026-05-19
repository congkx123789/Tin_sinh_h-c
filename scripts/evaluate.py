import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lifelines.utils import concordance_index
from utils.metrics import calculate_km_curve

def evaluate(data_split="test_internal"):
    print(f"🚀 Starting Evaluation on {data_split} using Improved LightGBM...")
    
    # Mapping for data structure
    path_mapping = {
        "test_internal": "training/test_internal",
        "test_lgg": "validation/TCGA_LGG",
        "test_cgga": "validation/CGGA_693",
        "test_cgga_325": "validation/CGGA_325",
        "test_rembrandt": "validation/REMBRANDT",
        "test_gse4271": "validation/GSE4271",
        "test_gse7696": "validation/GSE7696",
        "test_gse13041": "validation/GSE13041",
        "test_gse4412": "validation/GSE4412"
    }
    
    target_path = path_mapping.get(data_split, f"validation/{data_split}")
    data_dir = os.path.join("data/02_processed", target_path)
    
    X_test_path = os.path.join(data_dir, "X.csv")
    y_test_path = os.path.join(data_dir, "y.csv")
    
    if not os.path.exists(X_test_path):
        print(f"❌ Error: Test data not found at {X_test_path}.")
        return
        
    X_test_df = pd.read_csv(X_test_path, index_col=0)
    y_test_df = pd.read_csv(y_test_path, index_col=0)
    
    # --- 1. Load Ensemble Model and Scaler ---
    model_path = "checkpoints/lightgbm_weights/best_ensemble.pkl"
    if os.path.exists(model_path):
        try:
            with open(model_path, "rb") as f:
                ensemble_data = pickle.load(f)
            models = ensemble_data['models']
            scaler = ensemble_data['scaler']
            selected_genes = ensemble_data['genes']
            invert = ensemble_data.get('invert', False)
            print("✅ Loaded Ensemble models, scaler, and selected genes.")
        except Exception as e:
            print(f"❌ Error loading ensemble model: {e}")
            return
    else:
        print("❌ Error: Ensemble weights not found.")
        return

    # Check if all features exist in test data
    missing_features = [f for f in selected_genes if f not in X_test_df.columns]
    if missing_features:
        print(f"⚠️ Warning: {len(missing_features)} features missing in test set. Filling with 0.")
        for f in missing_features:
            X_test_df[f] = 0
            
    X_test_fs = X_test_df[selected_genes]
    X_test_scaled = scaler.transform(X_test_fs)
        
    # --- 4. Predict Risk Scores ---
    preds = np.mean([m.predict(X_test_scaled) for m in models], axis=0)
    if invert:
        risk_scores = preds
    else:
        risk_scores = -preds
         
    # --- 5. Calculate C-Index ---
    times = y_test_df['OS.time'].values
    events = y_test_df['OS'].values
    
    c_index = concordance_index(times, risk_scores, events)
    print(f"🔥 {data_split} C-index: {c_index:.4f}")
    
    # --- 6. Kaplan-Meier Visualization ---
    median_risk = np.median(risk_scores)
    high_risk_mask = (risk_scores >= median_risk)
    low_risk_mask = ~high_risk_mask
    
    plt.figure(figsize=(10, 6))
    
    # Low Risk Plot
    t_low, s_low = calculate_km_curve(times[low_risk_mask], events[low_risk_mask])
    plt.step(t_low, s_low, where='post', label=f'Low Risk (N={sum(low_risk_mask)})', color='blue')
    
    # High Risk Plot
    t_high, s_high = calculate_km_curve(times[high_risk_mask], events[high_risk_mask])
    plt.step(t_high, s_high, where='post', label=f'High Risk (N={sum(high_risk_mask)})', color='red')
    
    plt.title(f"Kaplan-Meier Survival Curves ({data_split} - Improved LightGBM)")
    plt.xlabel("Survival Time (Days)")
    plt.ylabel("Survival Probability")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Save Plot
    os.makedirs("results", exist_ok=True)
    plot_path = f"results/km_plot_{data_split}_lgbm_improved.png"
    plt.savefig(plot_path)
    print(f"✅ Evaluation complete. Kaplan-Meier plot saved to {plot_path}")

if __name__ == "__main__":
    import sys
    split = sys.argv[1] if len(sys.argv) > 1 else "test_internal"
    evaluate(split)
