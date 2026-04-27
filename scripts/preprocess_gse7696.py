import os
import gzip
import pandas as pd
import numpy as np
import io
import requests
from utils.preprocessing import log_transform, normalize_data

def fetch_probe_to_symbol(probe_ids, platform="reporter"):
    print(f"Fetching mapping for {len(probe_ids)} probes via MyGene.info...")
    url = "https://mygene.info/v3/query"
    chunk_size = 1000
    mapping_dict = {}
    for i in range(0, len(probe_ids), chunk_size):
        chunk = probe_ids[i:i + chunk_size]
        payload = {'q': chunk, 'scopes': platform, 'fields': 'symbol', 'species': 'human'}
        try:
            response = requests.post(url, json=payload)
            results = response.json()
            for item in results:
                if 'symbol' in item:
                    mapping_dict[item['query']] = item['symbol']
        except Exception as e:
            print(f"Error: {e}")
    return mapping_dict

def preprocess_gse7696():
    print("🚀 Starting data preprocessing for GSE7696...")
    matrix_path = "data/raw/GSE7696_matrix.gz"
    processed_dir = "data/processed/test_gse7696"
    os.makedirs(processed_dir, exist_ok=True)

    # 1. Load Ref Genes
    ref_genes = pd.read_csv("data/processed/train/X.csv", nrows=0).columns.tolist()[1:]

    # 2. Parse Matrix
    sample_ids = []
    characteristics = {}
    expression_lines = []
    expression_started = False

    with gzip.open(matrix_path, 'rt') as f:
        for line in f:
            if line.startswith('!Sample_geo_accession'):
                sample_ids = line.strip().split('\t')[1:]
                sample_ids = [s.strip('"') for s in sample_ids]
            elif line.startswith('!Sample_characteristics_ch1'):
                parts = line.strip().split('\t')
                vals = [p.strip('"') for p in parts[1:]]
                if ':' in vals[0]:
                    key = vals[0].split(':')[0].strip().lower()
                    characteristics[key] = [v.split(':')[-1].strip() if ':' in v else '' for v in vals]
            elif line.startswith('!series_matrix_table_begin'):
                expression_started = True
                continue
            if expression_started:
                if line.startswith('!series_matrix_table_end'):
                    break
                expression_lines.append(line)

    # Clinical extraction
    # Keys found: 'survival status', 'survival time in months'
    if 'survival progress' in characteristics: # Wait, I saw 'survival status' earlier
         pass
    
    # Correcting search for keys
    status_key = next((k for k in characteristics if 'survival status' in k), None)
    time_key = next((k for k in characteristics if 'survival time' in k), None)

    if not status_key or not time_key:
        print(f"❌ Error: Survival keys not found. Keys: {list(characteristics.keys())}")
        return

    clinical_df = pd.DataFrame({
        'sample': sample_ids,
        'OS.time': characteristics[time_key],
        'OS': characteristics[status_key]
    })
    clinical_df['OS.time'] = pd.to_numeric(clinical_df['OS.time'], errors='coerce') * 30.44
    clinical_df['OS'] = pd.to_numeric(clinical_df['OS'], errors='coerce')
    clinical_df = clinical_df.dropna()
    clinical_df.set_index('sample', inplace=True)

    # 3. Load Expression
    expr_df = pd.read_csv(io.StringIO("".join(expression_lines)), sep='\t', index_col=0)
    expr_df.columns = [c.strip('"') for c in expr_df.columns]
    
    common_samples = expr_df.columns.intersection(clinical_df.index)
    expr_df = expr_df[common_samples]
    y = clinical_df.loc[common_samples][['OS.time', 'OS']]

    # 4. Map Probes
    probes = expr_df.index.tolist()
    mapping_dict = fetch_probe_to_symbol(probes)
    mapping_df = pd.DataFrame(list(mapping_dict.items()), columns=['probe', 'symbol'])
    
    expr_df = expr_df.reset_index().rename(columns={'ID_REF': 'probe'})
    expr_df = expr_df.merge(mapping_df, on='probe')
    expr_df = expr_df.drop(columns=['probe']).groupby('symbol').mean()
    X = expr_df.T

    # 5. Normalize
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

    # 6. Save
    X_aligned.to_csv(os.path.join(processed_dir, "X.csv"))
    y.to_csv(os.path.join(processed_dir, "y.csv"))
    print(f"✅ GSE7696 processed. Shape: {X_aligned.shape}")

if __name__ == "__main__":
    preprocess_gse7696()
