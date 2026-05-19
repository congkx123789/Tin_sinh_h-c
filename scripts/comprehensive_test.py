import os
import pandas as pd
import numpy as np
import pickle
from lifelines.utils import concordance_index

def run_comprehensive_evaluation():
    print("🚀 Running Comprehensive Multi-cohort Validation...")
    
    # 1. Define Cohorts
    cohorts = {
        "TCGA-GBM (Internal)": "training/test_internal",
        "TCGA-LGG (External)": "validation/TCGA_LGG",
        "CGGA-693 (External)": "validation/CGGA_693",
        "REMBRANDT (External)": "validation/REMBRANDT",
        "GSE4412 (External)": "validation/GSE4412"
    }
    
    # 2. Load Model and Features
    try:
        with open("checkpoints/lightgbm_weights/best_ensemble.pkl", "rb") as f:
            ensemble_data = pickle.load(f)
        models = ensemble_data['models']
        scaler = ensemble_data['scaler']
        selected_genes = ensemble_data['genes']
        invert = ensemble_data.get('invert', False)
        print("✅ Ensemble models, scaler, and selected genes loaded.")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return

    results = []

    # 3. Evaluate each cohort
    for name, path in cohorts.items():
        data_dir = os.path.join("data/02_processed", path)
        X_path = os.path.join(data_dir, "X.csv")
        y_path = os.path.join(data_dir, "y.csv")
        
        if not os.path.exists(X_path):
            print(f"⚠️ Warning: Data for {name} not found. Skipping.")
            continue
            
        X_test = pd.read_csv(X_path, index_col=0)
        y_test = pd.read_csv(y_path, index_col=0)
        
        # Prepare features (match ensemble genes)
        for g in selected_genes:
            if g not in X_test.columns:
                X_test[g] = 0
                
        X_final = X_test[selected_genes]
        X_final_scaled = scaler.transform(X_final)
        
        # Predict
        preds = np.mean([m.predict(X_final_scaled) for m in models], axis=0)
        if invert:
             risk_scores = preds
        else:
             risk_scores = -preds
        
        # C-index
        c_index = concordance_index(y_test['OS.time'], risk_scores, y_test['OS'])
        results.append({"Cohort": name, "C-index": round(c_index, 4)})
        print(f"✅ {name}: C-index = {c_index:.4f}")

    # 4. Save and Summary
    res_df = pd.DataFrame(results)
    os.makedirs("results", exist_ok=True)
    res_df.to_csv("results/multi_cohort_results.csv", index=False)
    
    print("\n--- Summary Table ---")
    print(res_df.to_string(index=False))
    print("\n✅ Multi-cohort validation complete. Saved to results/multi_cohort_results.csv")

if __name__ == "__main__":
    run_comprehensive_evaluation()
