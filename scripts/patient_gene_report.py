import os
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet

def generate_individual_report(dataset_path, patient_idx=0):
    print(f"🧬 Generating Detailed Gene Report for Patient Index {patient_idx}...")
    
    # 1. Load Data
    df = pd.read_csv(dataset_path, index_col=0)
    patient_id = df.index[patient_idx]
    patient_data = torch.tensor(df.iloc[patient_idx:patient_idx+1].values, dtype=torch.float32, requires_grad=True)
    
    # 2. Load Model
    input_dim = 16383
    latent_dim = 128
    ae = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    model = SurvivalMambaNet(encoder=ae.encoder, latent_dim=latent_dim)
    model.load_state_dict(torch.load("checkpoints/mamba_weights/best_classifier.pth"))
    model.eval()

    # 3. Calculate Gradients (Explainability)
    # We want to see how each gene affects the probability output
    prob = model(patient_data, mode='classification')
    prob.backward()
    
    # Gradients represent the importance of each gene for THIS specific patient
    importances = patient_data.grad.squeeze().numpy()
    gene_names = df.columns.tolist()
    
    # Combine into a DataFrame
    importance_df = pd.DataFrame({
        'Gene': gene_names,
        'Importance': importances,
        'Expression': df.iloc[patient_idx].values
    })
    
    # Sort by importance
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    
    # Top 10 High-Risk Genes (Positive Importance)
    top_high_risk = importance_df.head(10)
    # Top 10 Protective Genes (Negative Importance)
    top_protective = importance_df.tail(10)
    
    # 4. Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    
    # Plot High-Risk Genes
    sns.barplot(data=top_high_risk, x='Importance', y='Gene', palette='Reds_r', ax=ax1)
    ax1.set_title(f"Top 10 High-Risk Drivers\n(Genes pushing risk UP)")
    
    # Plot Protective Genes
    sns.barplot(data=top_protective, x='Importance', y='Gene', palette='Greens', ax=ax2)
    ax2.set_title(f"Top 10 Protective Factors\n(Genes pushing risk DOWN)")
    
    plt.suptitle(f"Personalized Gene Diagnostic Report: {patient_id}\nAI Prediction Prob: {prob.item()*100:.2f}%", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    report_path = f"results/patient_report_{patient_id}.png"
    os.makedirs("results", exist_ok=True)
    plt.savefig(report_path)
    plt.close()
    
    print(f"✅ Report generated: {report_path}")
    print("\n--- Top 5 Dangerous Genes identified for this patient ---")
    print(top_high_risk[['Gene', 'Importance']].head(5).to_string(index=False))
    
    return report_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to X.csv")
    parser.add_argument("--idx", type=int, default=0, help="Patient index")
    args = parser.parse_args()
    
    generate_individual_report(args.file, args.idx)
