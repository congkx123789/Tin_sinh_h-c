import os
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet

def extract_biomarkers():
    print("🚀 Starting Biomarker Extraction...")
    
    data_dir = "data/02_processed/training/train"
    X_path = os.path.join(data_dir, "X.csv")
    
    if not os.path.exists(X_path):
        print("❌ Error: Test data not found.")
        return
        
    X_df = pd.read_csv(X_path, index_col=0)
    
    # Reconstruct Model
    input_dim = X_df.shape[1]
    latent_dim = 128
    
    ae = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    model = SurvivalMambaNet(encoder=ae.encoder, latent_dim=latent_dim)
    
    # Load Weights
    mamba_weights = "checkpoints/mamba_weights/best_mamba.pth"
    if os.path.exists(mamba_weights):
        model.load_state_dict(torch.load(mamba_weights))
        print("✅ Loaded model weights.")
    else:
        print("❌ Error: Model weights not found. Train the model first.")
        return
        
    model.eval()
    
    # Predict Risk Scores
    X_tensor = torch.tensor(X_df.values, dtype=torch.float32)
    with torch.no_grad():
        risk_scores = model(X_tensor).squeeze().numpy()
        
    print(f"Calculating correlations for {input_dim} genes...")
    
    correlations = []
    gene_names = X_df.columns.tolist()
    X_numpy = X_df.values
    
    for i in range(input_dim):
        gene_expr = X_numpy[:, i]
        # Ignore constant genes
        if np.std(gene_expr) == 0:
            corr = 0
        else:
            corr, _ = pearsonr(gene_expr, risk_scores)
        correlations.append(corr)
        
    # Create DataFrame
    corr_df = pd.DataFrame({
        'Gene': gene_names,
        'Correlation_with_Risk': correlations
    })
    
    corr_df = corr_df.dropna().sort_values(by='Correlation_with_Risk', ascending=False)
    
    top_positive = corr_df.head(20).copy()
    top_positive['Type'] = 'Malignant (Increases Risk)'
    
    top_negative = corr_df.tail(20).copy()
    top_negative['Type'] = 'Protective (Decreases Risk)'
    
    biomarkers_df = pd.concat([top_positive, top_negative])
    
    os.makedirs("results", exist_ok=True)
    csv_path = "results/biomarker_genes.csv"
    biomarkers_df.to_csv(csv_path, index=False)
    print(f"✅ Extracted top 40 biomarkers. Saved to {csv_path}")
    
    # Plotting
    plt.figure(figsize=(14, 10))
    
    # Sort for plotting: negative first, then positive
    plot_df = pd.concat([top_negative, top_positive.sort_values(by='Correlation_with_Risk', ascending=True)])
    
    colors = ['skyblue' if c < 0 else 'salmon' for c in plot_df['Correlation_with_Risk']]
    
    plt.barh(plot_df['Gene'], plot_df['Correlation_with_Risk'], color=colors)
    plt.axvline(0, color='black', linewidth=1)
    
    plt.title("Top 20 Protective vs Top 20 Malignant Genes (Mamba Risk Score Correlation)")
    plt.xlabel("Pearson Correlation Coefficient")
    plt.ylabel("Gene Symbol")
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    
    plot_path = "results/biomarker_importance.png"
    plt.savefig(plot_path, bbox_inches='tight')
    print(f"✅ Biomarker plot saved to {plot_path}")

if __name__ == "__main__":
    extract_biomarkers()
