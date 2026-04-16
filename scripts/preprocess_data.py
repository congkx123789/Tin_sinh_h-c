import os
import pandas as pd
import numpy as np
from utils.preprocessing import filter_genes, log_transform, normalize_data, map_ensembl_to_symbol

def preprocess_tcga_data():
    print("🚀 Starting data preprocessing for TCGA-GBM...")
    
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)

    # 1. Load RNA-Seq and Mapping Data
    print("Loading RNA-Seq and Gene Mapping data...")
    rna_path = os.path.join(raw_dir, "gbm_rna_seq.tsv.gz")
    mapping_path = os.path.join(raw_dir, "gencode_probemap.tsv")
    
    rna_df = pd.read_csv(rna_path, sep='\t', index_col=0)
    
    mapping_df = None
    if os.path.exists(mapping_path):
        try:
            # Check if it's a valid TSV by reading first line
            with open(mapping_path, 'r') as f:
                first_line = f.readline()
                if not first_line.startswith('<?xml'):
                    mapping_df = pd.read_csv(mapping_path, sep='\t')
                else:
                    print("Warning: gencode_probemap.tsv is corrupted (XML error). Will fetch from API.")
        except Exception as e:
            print(f"Warning: Could not load mapping file: {e}. Will fetch from API.")
    
    # Transpose so rows = patients, columns = genes
    rna_df = rna_df.T
    print(f"Original RNA-Seq shape: {rna_df.shape}")

    # 2. Map Ensembl IDs to Gene Symbols
    print("Mapping Ensembl IDs to Gene Symbols...")
    rna_df = map_ensembl_to_symbol(rna_df, mapping_df)
    print(f"RNA-Seq shape after mapping: {rna_df.shape}")

    # 3. Load Survival Data (The Golden Labels)
    print("Loading Survival data...")
    survival_path = os.path.join(raw_dir, "gbm_survival.tsv.gz")
    survival_df = pd.read_csv(survival_path, sep='\t')
    # Required columns: 'sample', 'OS', 'OS.time'
    survival_df = survival_df[['sample', 'OS', 'OS.time']].dropna()
    survival_df.set_index('sample', inplace=True)
    print(f"Original Survival data shape: {survival_df.shape}")

    # 3. Intersection of Patient IDs
    print("Finding intersection of samples...")
    common_samples = rna_df.index.intersection(survival_df.index)
    X = rna_df.loc[common_samples]
    y = survival_df.loc[common_samples]
    
    print(f"Matched Shared samples: {len(common_samples)}")

    # 4. Filter Genes and Normalize
    print("Filtering genes and normalizing...")
    # Filter low variance genes
    X = filter_genes(X, variance_threshold=0.1)
    # Log-transform and normalize
    X = log_transform(X)
    X = normalize_data(X)

    # 5. Stratified Train/Val/Test Split (70/15/15)
    print("Splitting data into Stratified Train/Val/Test sets...")
    from sklearn.model_selection import train_test_split
    
    # First split: Tách Test set (15%)
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, 
        test_size=0.15, 
        stratify=y['OS'], 
        random_state=42
    )
    
    # Second split: Tách Train (70%) và Val (15%) từ phần còn lại (85%)
    # val_size = 15 / 85 ≈ 0.176
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, 
        test_size=0.1765, 
        stratify=y_temp['OS'], 
        random_state=42
    )

    # 6. Save Processed Data
    print(f"Final training set shape: {X_train.shape}")
    print(f"Final validation set shape: {X_val.shape}")
    print(f"Final test set shape: {X_test.shape}")
    
    # Save all splits
    X_train.to_csv(os.path.join(processed_dir, "X_train.csv"))
    y_train.to_csv(os.path.join(processed_dir, "y_train.csv"))
    X_val.to_csv(os.path.join(processed_dir, "X_val.csv"))
    y_val.to_csv(os.path.join(processed_dir, "y_val.csv"))
    X_test.to_csv(os.path.join(processed_dir, "X_test.csv"))
    y_test.to_csv(os.path.join(processed_dir, "y_test.csv"))
    
    # Also keep X_final for backwards compatibility or full-set runs
    X.to_csv(os.path.join(processed_dir, "X_final.csv"))
    y.to_csv(os.path.join(processed_dir, "y_final.csv"))
    
    print("✅ Preprocessing complete! Files saved to data/processed/")

if __name__ == "__main__":
    preprocess_tcga_data()
