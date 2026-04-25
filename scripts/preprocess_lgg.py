import os
import pandas as pd
import numpy as np
from utils.preprocessing import filter_genes, log_transform, normalize_data, map_ensembl_to_symbol

def preprocess_lgg():
    print("🚀 Preprocessing LGG data for GBM model validation...")
    
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    
    rna_path = os.path.join(raw_dir, "lgg_rna_seq.tsv.gz")
    survival_path = os.path.join(raw_dir, "lgg_survival.tsv.gz")
    features_path = os.path.join(processed_dir, "gbm_features.txt")
    
    if not os.path.exists(rna_path) or not os.path.exists(survival_path):
        print("❌ Error: LGG data not found. Wait for download.")
        return

    # 1. Load Data
    print("Loading LGG RNA-Seq...")
    rna_df = pd.read_csv(rna_path, sep='\t', index_col=0).T
    
    print("Loading LGG Survival...")
    survival_df = pd.read_csv(survival_path, sep='\t')
    survival_df = survival_df[['sample', 'OS', 'OS.time']].dropna()
    survival_df.set_index('sample', inplace=True)

    # 2. Map to Symbols
    print("Mapping LGG Ensembl IDs to Symbols...")
    rna_df = map_ensembl_to_symbol(rna_df)
    
    # 3. Intersection
    print("Finding intersection...")
    common_samples = rna_df.index.intersection(survival_df.index)
    X = rna_df.loc[common_samples]
    y = survival_df.loc[common_samples]

    # 4. Feature Alignment (CRITICAL)
    print("Aligning features with GBM model...")
    with open(features_path, 'r') as f:
        gbm_features = [line.strip() for line in f.readlines()]
    
    # Reindex to match GBM features, fill missing with 0
    X = X.reindex(columns=gbm_features, fill_value=0)
    print(f"Alignment complete. Shape: {X.shape}")

    # 5. Normalize
    X = log_transform(X)
    X = normalize_data(X)

    # 6. Save in dedicated subfolder
    test_lgg_dir = os.path.join(processed_dir, "test_lgg")
    os.makedirs(test_lgg_dir, exist_ok=True)
    
    X.to_csv(os.path.join(test_lgg_dir, "X.csv"))
    y.to_csv(os.path.join(test_lgg_dir, "y.csv"))
    print("✅ LGG Validation data ready at data/processed/test_lgg/")

if __name__ == "__main__":
    preprocess_lgg()
