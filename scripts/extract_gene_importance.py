import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def extract_importance():
    print("🚀 Extracting Gene Importance from Optimized LightGBM Pipeline...")
    
    # 1. Load Selected Genes
    selection_path = "checkpoints/lightgbm_weights/selected_genes.pkl"
    if not os.path.exists(selection_path):
        print("❌ Error: Selected genes file not found.")
        return
    with open(selection_path, "rb") as f:
        selected_genes = pickle.load(f)

    # 2. Load Ensemble Model
    model_path = "checkpoints/lightgbm_weights/best_ensemble.pkl"
    if not os.path.exists(model_path):
        print("❌ Error: Ensemble model file not found.")
        return
    with open(model_path, "rb") as f:
        ensemble_data = pickle.load(f)
    models = ensemble_data['models']
    selected_genes = ensemble_data['genes']

    # 3. Get Feature Importance (Averaged across ensemble models)
    # We use 'gain' as it's more representative of the contribution to the model
    all_importances = []
    for m in models:
        all_importances.append(m.feature_importance(importance_type='gain'))
    importances = np.mean(all_importances, axis=0)
    
    importance_df = pd.DataFrame({
        'Gene': selected_genes,
        'Importance (Gain)': importances
    }).sort_values(by='Importance (Gain)', ascending=False)

    # 4. Determine Direction (Correlation with Survival Time)
    # Load training data to calculate correlation
    X_train = pd.read_csv("data/02_processed/training/train/X.csv", index_col=0)
    y_train = pd.read_csv("data/02_processed/training/train/y.csv", index_col=0)
    
    print("\n--- Top Genes Affecting Survival ---")
    results = []
    for i, row in importance_df.head(20).iterrows():
        gene = row['Gene']
        gain = row['Importance (Gain)']
        
        # Calculate correlation with OS.time
        if gene in X_train.columns:
            corr = X_train[gene].corr(y_train['OS.time'])
            impact = "Protective (Lives Longer)" if corr > 0 else "Malignant (Dies Sooner)"
            results.append({
                'Gene': gene,
                'Importance': gain,
                'Correlation': corr,
                'Impact': impact
            })
        else:
            results.append({
                'Gene': gene,
                'Importance': gain,
                'Correlation': 0,
                'Impact': "Clinical Feature"
            })

    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))

    # Save to CSV for the user
    os.makedirs("results", exist_ok=True)
    results_df.to_csv("results/top_genes_importance.csv", index=False)
    
    # Visualization
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Gene', data=results_df, palette='viridis')
    plt.title('Top 20 Genes by Importance (LightGBM Gain)')
    plt.xlabel('Importance (Gain)')
    plt.ylabel('Gene Symbol')
    plt.tight_layout()
    plt.savefig("results/gene_importance_plot.png")
    
    print(f"\n✅ Results saved to results/top_genes_importance.csv")
    print(f"✅ Visualization saved to results/gene_importance_plot.png")

if __name__ == "__main__":
    extract_importance()
