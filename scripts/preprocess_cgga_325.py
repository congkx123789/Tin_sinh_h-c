import os
import pandas as pd
import numpy as np
from utils.preprocessing import log_transform, normalize_data

def preprocess_cgga_325_data():
    print("🚀 Starting data preprocessing for CGGA-325...")
    
    raw_dir = "data/raw/cgga_325"
    processed_dir = "data/processed/test_cgga_325"
    os.makedirs(processed_dir, exist_ok=True)

    # 1. Load Reference Genes from Training Data
    print("Loading reference gene list (16,504 genes)...")
    train_x_path = "data/processed/train/X.csv"
    if not os.path.exists(train_x_path):
        print("❌ Error: Training data (X.csv) not found. Cannot align features.")
        return
    
    ref_genes = pd.read_csv(train_x_path, nrows=0).columns.tolist()
    if ref_genes[0] == "Unnamed: 0" or ref_genes[0] == "":
        ref_genes = ref_genes[1:]
    
    print(f"Reference genes count: {len(ref_genes)}")

    # 2. Load CGGA 325 Expression Data
    print("Loading CGGA mRNA-seq 325 expression data...")
    expr_path = os.path.join(raw_dir, "CGGA.mRNAseq_325.RSEM-genes.20200506.txt")
    expr_df = pd.read_csv(expr_path, sep='\t', index_col=0)
    
    # Transpose so rows = patients, columns = genes
    expr_df = expr_df.T
    print(f"Original CGGA Expression shape: {expr_df.shape}")

    # 3. Load CGGA 325 Clinical Data
    print("Loading CGGA clinical data...")
    clinical_path = os.path.join(raw_dir, "CGGA.mRNAseq_325_clinical.20200506.txt")
    clinical_df = pd.read_csv(clinical_path, sep='\t')
    
    # Required columns: 'CGGA_ID', 'OS', 'Censor (alive=0; dead=1)'
    clinical_df = clinical_df[['CGGA_ID', 'OS', 'Censor (alive=0; dead=1)']].dropna()
    clinical_df.columns = ['sample', 'OS.time', 'OS']
    clinical_df.set_index('sample', inplace=True)
    print(f"Original Clinical data shape: {clinical_df.shape}")

    # 4. Intersection of Patient IDs
    print("Finding intersection of samples...")
    common_samples = expr_df.index.intersection(clinical_df.index)
    X = expr_df.loc[common_samples]
    y = clinical_df.loc[common_samples]
    print(f"Matched Shared samples: {len(common_samples)}")

    # 5. Feature Alignment (16,504 genes)
    print("Aligning genes with reference list...")
    intersect_genes = [g for g in ref_genes if g in X.columns]
    missing_genes = [g for g in ref_genes if g not in X.columns]
    
    print(f"Found {len(intersect_genes)} out of {len(ref_genes)} reference genes.")
    print(f"Missing {len(missing_genes)} genes. Filling with 0.")
    
    X_aligned = X[intersect_genes].copy()
    
    if missing_genes:
        missing_df = pd.DataFrame(0, index=X_aligned.index, columns=missing_genes)
        X_aligned = pd.concat([X_aligned, missing_df], axis=1)
    
    # Final reorder
    X_aligned = X_aligned[ref_genes]
    print(f"Final aligned shape: {X_aligned.shape}")

    # 6. Normalize
    print("Applying log transformation and normalization...")
    X_aligned = log_transform(X_aligned)
    X_aligned = normalize_data(X_aligned)

    # 7. Save
    X_aligned.to_csv(os.path.join(processed_dir, "X.csv"))
    y.to_csv(os.path.join(processed_dir, "y.csv"))
    print(f"✅ Processed CGGA-325 data saved to {processed_dir}")

if __name__ == "__main__":
    preprocess_cgga_325_data()
