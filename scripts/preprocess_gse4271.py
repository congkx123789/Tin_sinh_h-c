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

def preprocess_gse4271():
    print("🚀 Starting data preprocessing for GSE4271...")
    matrix_path = "data/raw/GSE4271_matrix.gz"
    processed_dir = "data/processed/test_gse4271"
    os.makedirs(processed_dir, exist_ok=True)

    # 1. Load Ref Genes
    ref_genes = pd.read_csv("data/processed/train/X.csv", nrows=0).columns.tolist()[1:]

    # 2. Parse Matrix for metadata and expression
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
    # Keys found earlier: 'survival (weeks)', 'censor'
    if 'survival (weeks)' not in characteristics or 'censor' not in characteristics:
        print(f"❌ Error: Required clinical keys not found. Keys: {list(characteristics.keys())}")
        return

    clinical_df = pd.DataFrame({
        'sample': sample_ids,
        'OS.time': characteristics['survival (weeks)'],
        'OS_censor': characteristics['censor']
    })
    clinical_df['OS.time'] = pd.to_numeric(clinical_df['OS.time'], errors='coerce') * 7 # Weeks to days
    # Censor: 'no' means dead (event occurs), 'yes' means censored? Wait, usually censor means alive.
    # Let's verify for GSE4271: "censor: yes" usually means patient is alive.
    clinical_df['OS'] = clinical_df['OS_censor'].apply(lambda x: 1 if str(x).lower() == 'no' else 0)
    clinical_df = clinical_df.dropna(subset=['OS.time', 'OS'])
    clinical_df.set_index('sample', inplace=True)

    # 3. Load Expression
    expr_df = pd.read_csv(io.StringIO("".join(expression_lines)), sep='\t', index_col=0)
    expr_df.columns = [c.strip('"') for c in expr_df.columns]
    
    # Common samples
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

    # 5. Align
    intersect_genes = [g for g in ref_genes if g in X.columns]
    missing_genes = [g for g in ref_genes if g not in X.columns]
    print(f"Matched {len(intersect_genes)} genes. Missing {len(missing_genes)}.")
    
    X_aligned = X[intersect_genes].copy()
    if missing_genes:
        missing_df = pd.DataFrame(0, index=X_aligned.index, columns=missing_genes)
        X_aligned = pd.concat([X_aligned, missing_df], axis=1)
    
    X_aligned = X_aligned[ref_genes]
    X_aligned = log_transform(X_aligned)
    X_aligned = normalize_data(X_aligned)

    # 6. Save
    X_aligned.to_csv(os.path.join(processed_dir, "X.csv"))
    y.to_csv(os.path.join(processed_dir, "y.csv"))
    print(f"✅ GSE4271 processed. Shape: {X_aligned.shape}")

if __name__ == "__main__":
    preprocess_gse4271()
