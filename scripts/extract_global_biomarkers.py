import os
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet

def extract_global_biomarkers():
    print("🌍 Extracting Global Biomarkers (Universal Malignant/Protective Genes)...")
    
    # 1. Load Data
    X_train_path = "data/02_processed/training/train/X.csv"
    X_df = pd.read_csv(X_train_path, index_col=0)
    X_tensor = torch.tensor(X_df.values, dtype=torch.float32, requires_grad=True)
    
    # 2. Load Model
    input_dim = 16383
    latent_dim = 128
    ae = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    model = SurvivalMambaNet(encoder=ae.encoder, latent_dim=latent_dim)
    model.load_state_dict(torch.load("checkpoints/mamba_weights/best_classifier.pth"))
    model.eval()

    # 3. Calculate Global Importance (Mean Gradients across all patients)
    probs = model(X_tensor, mode='classification')
    # Backward pass for the sum of probabilities to get average influence
    probs.sum().backward()
    
    importances = X_tensor.grad.mean(dim=0).numpy()
    gene_names = X_df.columns.tolist()
    
    # Combine into a DataFrame
    global_importance = pd.DataFrame({
        'Gene': gene_names,
        'Global_Importance': importances
    })
    
    # Sort
    global_importance = global_importance.sort_values(by='Global_Importance', ascending=False)
    
    # Top 20 Malignant (Risk-increasing)
    top_malignant = global_importance.head(20)
    # Top 20 Protective (Survival-increasing)
    top_protective = global_importance.tail(20)
    
    # 4. Save results
    results_dir = "results/biomarkers"
    os.makedirs(results_dir, exist_ok=True)
    global_importance.to_csv(os.path.join(results_dir, "global_biomarkers.csv"), index=False)
    
    # 5. Visualization
    plt.figure(figsize=(12, 10))
    
    # We'll plot the top 20 malignant genes
    sns.barplot(data=top_malignant, x='Global_Importance', y='Gene', palette='OrRd_r')
    plt.title("Top 20 GLOBAL Malignant Genes (The 'Death Signature')\nGenes that most consistently increase risk across all patients", fontsize=14)
    plt.xlabel("Average Importance Score")
    plt.tight_layout()
    
    plot_path = os.path.join(results_dir, "global_malignant_genes.png")
    plt.savefig(plot_path)
    plt.close()
    
    print(f"✅ Global Biomarkers extracted and saved to {results_dir}")
    print("\n--- TOP 10 MOST DANGEROUS GENES (GLOBAL) ---")
    print(top_malignant.head(10).to_string(index=False))
    
    return plot_path

if __name__ == "__main__":
    extract_global_biomarkers()
