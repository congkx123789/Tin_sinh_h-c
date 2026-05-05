import os
import pandas as pd
import numpy as np
from utils.preprocessing import RNASeqCleaner, map_ensembl_to_symbol

def preprocess_tcga_data():
    print("🚀 Starting data preprocessing for TCGA-GBM...")
    
    raw_dir = "data/01_raw/TCGA"
    processed_dir = "data/02_processed/training"
    metadata_dir = "data/03_metadata"
    os.makedirs(processed_dir, exist_ok=True)

    # 1. Load RNA-Seq and Mapping Data
    print("Loading RNA-Seq and Gene Mapping data...")
    rna_path = os.path.join(raw_dir, "gbm_rna_seq.tsv.gz")
    mapping_path = os.path.join(metadata_dir, "gencode_probemap.tsv")
    
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
    
    # Load Clinical data for Treatment info
    print("Loading Clinical data for Treatment info...")
    clinical_path = os.path.join(raw_dir, "gbm_clinical.tsv.gz")
    if os.path.exists(clinical_path):
        clinical_df = pd.read_csv(clinical_path, sep='\t')
        if 'submitter_id' in clinical_df.columns and 'treatment_type.treatments.diagnoses' in clinical_df.columns:
            clin_subset = clinical_df[['submitter_id', 'treatment_type.treatments.diagnoses']].copy()
            clin_subset.rename(columns={'treatment_type.treatments.diagnoses': 'Treatment'}, inplace=True)
            clin_subset = clin_subset.drop_duplicates(subset=['submitter_id'])
            
            # Extract patient ID from sample (e.g., 'TCGA-15-1447-01A' -> 'TCGA-15-1447')
            survival_df['submitter_id'] = survival_df['sample'].str[:12]
            survival_df = pd.merge(survival_df, clin_subset, on='submitter_id', how='left')
            survival_df.drop(columns=['submitter_id'], inplace=True)
            
            # Simplify Treatment column (if it contains 'Radiation', mark as Radiation, etc.)
            def simplify_treatment(t):
                if pd.isna(t):
                    return 'Unknown'
                t_str = str(t).lower()
                if 'radiation' in t_str and 'pharmaceutical' in t_str:
                    return 'Chemo+Radiation'
                elif 'radiation' in t_str:
                    return 'Radiation'
                elif 'pharmaceutical' in t_str:
                    return 'Chemotherapy'
                else:
                    return 'Other/None'
            survival_df['Treatment'] = survival_df['Treatment'].apply(simplify_treatment)

    survival_df.set_index('sample', inplace=True)
    print(f"Original Survival data shape: {survival_df.shape}")

    # 3. Intersection of Patient IDs
    print("Finding intersection of samples...")
    common_samples = rna_df.index.intersection(survival_df.index)
    X = rna_df.loc[common_samples]
    y = survival_df.loc[common_samples]
    
    print(f"Matched Shared samples: {len(common_samples)}")

    # 4. Filter Genes and Normalize with Advanced Pipeline
    print("Applying Advanced RNA-Seq Cleaning Pipeline...")
    cleaner = RNASeqCleaner(variance_threshold=0.1, expression_ratio=0.2)
    X_clean, inlier_mask = cleaner.fit_transform(X)
    
    # Save cleaner state for validation sets
    cleaner.save_state(os.path.join(processed_dir, "scaler.pkl"))
    
    # Filter out outlier patients from y
    y_clean = y.iloc[inlier_mask]
    
    print(f"Final Matched Clean Samples: {X_clean.shape[0]}")

    # 5. Stratified Train/Val/Test Split (70/15/15)
    print("Splitting data into Stratified Train/Val/Test sets...")
    from sklearn.model_selection import train_test_split
    
    # First split: Tách Test set (15%)
    X_temp, X_test, y_temp, y_test = train_test_split(
        X_clean, y_clean, 
        test_size=0.15, 
        stratify=y_clean['OS'], 
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

    # 6. Save Processed Data into subfolders
    print(f"Final training set shape: {X_train.shape}")
    print(f"Final validation set shape: {X_val.shape}")
    print(f"Final test set shape: {X_test.shape}")
    
    # Define subdirectories
    train_dir = os.path.join(processed_dir, "train")
    val_dir = os.path.join(processed_dir, "val")
    test_dir = os.path.join(processed_dir, "test_internal")
    
    for d in [train_dir, val_dir, test_dir]:
        os.makedirs(d, exist_ok=True)
    
    # Save splits
    X_train.to_csv(os.path.join(train_dir, "X.csv"))
    y_train.to_csv(os.path.join(train_dir, "y.csv"))
    X_val.to_csv(os.path.join(val_dir, "X.csv"))
    y_val.to_csv(os.path.join(val_dir, "y.csv"))
    X_test.to_csv(os.path.join(test_dir, "X.csv"))
    y_test.to_csv(os.path.join(test_dir, "y.csv"))
    
    print("✅ Preprocessing complete! Files organized into data/02_processed/training/[train, val, test_internal]")

if __name__ == "__main__":
    preprocess_tcga_data()
