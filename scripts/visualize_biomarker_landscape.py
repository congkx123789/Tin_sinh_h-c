import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_landscape():
    print("🎨 Generating Biomarker Landscape Dashboard...")
    
    # 1. Load the biomarker data we extracted earlier
    csv_path = "results/biomarkers/global_biomarkers.csv"
    if not os.path.exists(csv_path):
        print("❌ Biomarker CSV not found. Run extract_global_biomarkers.py first.")
        return
        
    df = pd.read_csv(csv_path)
    top_malignant = df.head(20)
    top_protective = df.tail(20)
    
    # 2. Setup Figure
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(2, 2)
    
    # Ax1: Malignant Genes (Red)
    ax1 = fig.add_subplot(gs[0, 0])
    sns.barplot(data=top_malignant, x='Global_Importance', y='Gene', palette='Reds_r', ax=ax1)
    ax1.set_title("🔥 TOP 20 MALIGNANT GENES (Death Signature)", fontsize=14, fontweight='bold')
    
    # Ax2: Protective Genes (Green)
    ax2 = fig.add_subplot(gs[0, 1])
    # Protective importance values are negative, we plot absolute for comparison or just use values
    sns.barplot(data=top_protective, x='Global_Importance', y='Gene', palette='Greens', ax=ax2)
    ax2.set_title("😇 TOP 20 PROTECTIVE GENES (Guardian Angels)", fontsize=14, fontweight='bold')
    
    # Ax3: Heatmap of Expression (Top 20 Malignant across top 50 patients)
    ax3 = fig.add_subplot(gs[1, :])
    
    # Load expression data to plot heatmap
    X_train = pd.read_csv("data/02_processed/training/train/X.csv", index_col=0)
    malignant_genes = top_malignant['Gene'].tolist()
    
    # Take first 50 patients and the top 20 genes
    heatmap_data = X_train.iloc[:50][malignant_genes].T
    
    sns.heatmap(heatmap_data, cmap='coolwarm', ax=ax3, cbar_kws={'label': 'Expression Level'})
    ax3.set_title("🌡️ Expression Heatmap: Top 20 Malignant Genes across 50 Patients", fontsize=14, fontweight='bold')
    ax3.set_xlabel("Patients")
    ax3.set_ylabel("Dangerous Genes")
    
    plt.suptitle("GBM BIOMARKER LANDSCAPE - AI DRIVEN ANALYSIS", fontsize=20, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    output_path = "results/biomarkers/biomarker_landscape_dashboard.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    print(f"✅ Landscape Dashboard generated: {output_path}")

if __name__ == "__main__":
    visualize_landscape()
