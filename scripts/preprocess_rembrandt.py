import os
import gzip
import pandas as pd
import numpy as np
import io
import requests
from utils.preprocessing import log_transform, normalize_data

def fetch_probe_to_symbol(probe_ids, platform="reporter"):
    """
    Fetch gene symbols for Affymetrix probes via MyGene.info API
    """
    print(f"Fetching mapping for {len(probe_ids)} probes via MyGene.info...")
    url = "https://mygene.info/v3/query"
    chunk_size = 1000
    mapping_dict = {}
    
    for i in range(0, len(probe_ids), chunk_size):
        chunk = probe_ids[i:i + chunk_size]
        payload = {
            'q': chunk,
            'scopes': platform,
            'fields': 'symbol',
            'species': 'human'
        }
        try:
            response = requests.post(url, json=payload)
            results = response.json()
            for item in results:
                if 'symbol' in item:
                    mapping_dict[item['query']] = item['symbol']
        except Exception as e:
            print(f"Error fetching symbols: {e}")
    return mapping_dict

def preprocess_rembrandt():
    print("🚀 Starting data preprocessing for REMBRANDT...")
    
    matrix_path = "data/raw/REMBRANDT_matrix.gz"
    clinical_path = "data/raw/REMBRANDT_clinical.txt.gz"
    processed_dir = "data/processed/test_rembrandt"
    os.makedirs(processed_dir, exist_ok=True)

    # 1. Load Reference Genes
    train_x_path = "data/processed/train/X.csv"
    ref_genes = pd.read_csv(train_x_path, nrows=0).columns.tolist()[1:]

    # 2. Parse Clinical Data
    print("Loading REMBRANDT clinical data...")
    clinical_df = pd.read_csv(clinical_path, sep='\t')
    clinical_df = clinical_df[['SUBJECT_ID', 'OVERALL_SURVIVAL_MONTHS', 'EVENT_OS']].dropna()
    clinical_df.columns = ['sample_title', 'OS.time', 'OS']
    # Convert months to days to match TCGA units
    clinical_df['OS.time'] = clinical_df['OS.time'] * 30.44
    clinical_df.set_index('sample_title', inplace=True)

    # 3. Parse Expression Matrix (Metadata only first)
    print("Parsing REMBRANDT expression matrix header for ID mapping...")
    sample_ids = []
    sample_titles = []
    expression_data_started = False
    expression_lines = []

    with gzip.open(matrix_path, 'rt') as f:
        for line in f:
            if line.startswith('!Sample_geo_accession'):
                sample_ids = line.strip().split('\t')[1:]
                sample_ids = [s.strip('"') for s in sample_ids]
            elif line.startswith('!Sample_title'):
                sample_titles = line.strip().split('\t')[1:]
                sample_titles = [s.strip('"') for s in sample_titles]
            elif line.startswith('!series_matrix_table_begin'):
                expression_data_started = True
                continue
            if expression_data_started:
                if line.startswith('!series_matrix_table_end'):
                    break
                expression_lines.append(line)

    # Map GSM IDs to Clinical Titles
    id_map = dict(zip(sample_ids, sample_titles))
    
    # 4. Load Expression Data
    print("Loading full expression matrix...")
    expr_df = pd.read_csv(io.StringIO("".join(expression_lines)), sep='\t', index_col=0)
    expr_df.columns = [id_map.get(c, c) for c in expr_df.columns]
    
    # Simple filtering: keep only samples in clinical data
    common_samples = expr_df.columns.intersection(clinical_df.index)
    expr_df = expr_df[common_samples]
    y = clinical_df.loc[common_samples]
    
    # 5. Map Probes to Symbols
    probes = expr_df.index.tolist()
    # To save time and API calls, we'll only fetch symbols for a subset or use a cached approach if possible
    # But for a robust solution, we fetch all.
    mapping_dict = fetch_probe_to_symbol(probes)
    
    mapping_df = pd.DataFrame(list(mapping_dict.items()), columns=['probe', 'symbol'])
    expr_df = expr_df.reset_index().rename(columns={'ID_REF': 'probe'})
    expr_df = expr_df.merge(mapping_df, on='probe')
    
    # Aggregate duplicate symbols
    expr_df = expr_df.drop(columns=['probe']).groupby('symbol').mean()
    X = expr_df.T # Rows=samples, Cols=genes

    # 6. Normalize
    # Prepare alignment
    intersect_genes = [g for g in ref_genes if g in X.columns]
    missing_genes = [g for g in ref_genes if g not in X.columns]
    print(f"Matched {len(intersect_genes)} genes. Missing {len(missing_genes)}.")

    # Check if data is already log-transformed (typical for some GEO matrices)
    if X.mean().mean() < 20:
        print("ℹ️ Data appears to be already log-transformed. Skipping log_transform.")
        X_aligned = X[intersect_genes].copy()
    else:
        print("ℹ️ Data appears to be in raw scale. Applying log_transform.")
        X_aligned = log_transform(X[intersect_genes].copy())
    
    if missing_genes:
        missing_df = pd.DataFrame(0, index=X_aligned.index, columns=missing_genes)
        X_aligned = pd.concat([X_aligned, missing_df], axis=1)
    
    X_aligned = X_aligned[ref_genes]
    X_aligned = normalize_data(X_aligned)

    # 7. Save
    X_aligned.to_csv(os.path.join(processed_dir, "X.csv"))
    y.to_csv(os.path.join(processed_dir, "y.csv"))
    print(f"✅ REMBRANDT processed. Shape: {X_aligned.shape}")

if __name__ == "__main__":
    preprocess_rembrandt()
