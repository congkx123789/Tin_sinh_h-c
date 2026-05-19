import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap

def explain():
    print("🚀 Explaining Optimized LightGBM Model with SHAP...")
    
    # 1. Load Data and Ensemble Model
    processed_dir = "data/02_processed/training"
    X_val = pd.read_csv(os.path.join(processed_dir, "val/X.csv"), index_col=0)
    
    try:
        with open("checkpoints/lightgbm_weights/best_ensemble.pkl", "rb") as f:
            ensemble_data = pickle.load(f)
        models = ensemble_data['models']
        scaler = ensemble_data['scaler']
        selected_genes = ensemble_data['genes']
        print("✅ Ensemble models, scaler, and selected genes loaded.")
    except Exception as e:
        print(f"❌ Error loading files: {e}")
        return

    # 2. Prepare and Scale Features
    # Ensure all selected genes exist
    for f in selected_genes:
        if f not in X_val.columns:
            X_val[f] = 0
            
    X_explain = X_val[selected_genes]
    X_explain_scaled = pd.DataFrame(scaler.transform(X_explain), columns=selected_genes)

    # 3. Initialize SHAP Explainer using the first model of the ensemble
    explainer = shap.TreeExplainer(models[0])
    shap_values = explainer.shap_values(X_explain_scaled)

    # Note: LightGBM SHAP values for regression are in the same scale as target (log-time).
    # Positive SHAP = increases predicted log-time = increases survival = PROTECTIVE.
    # Negative SHAP = decreases predicted log-time = decreases survival = MALIGNANT.

    # 4. Visualization: Summary Plot
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, X_explain, show=False)
    plt.title("SHAP Summary Plot: Gene Impact on Survival Time")
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/shap_summary_plot.png")
    print("✅ SHAP summary plot saved to results/shap_summary_plot.png")

    # 5. Visualization: Feature Importance (Mean SHAP)
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, X_explain, plot_type="bar", show=False)
    plt.title("Gene Importance based on Mean SHAP")
    plt.tight_layout()
    plt.savefig("results/shap_importance_plot.png")
    print("✅ SHAP importance plot saved to results/shap_importance_plot.png")

    # 6. Single Patient Explanation (Example)
    plt.figure(figsize=(12, 4))
    shap.plots.force(explainer.expected_value, shap_values[0,:], X_explain.iloc[0,:], matplotlib=True, show=False)
    plt.savefig("results/shap_force_plot_patient0.png")
    print("✅ Example patient force plot saved to results/shap_force_plot_patient0.png")

    print("\n--- SHAP Analysis Complete ---")
    print("Interpretation:")
    print("- RED dots on the RIGHT: High gene expression increases survival time (Protective).")
    print("- RED dots on the LEFT: High gene expression decreases survival time (Malignant).")

if __name__ == "__main__":
    explain()
