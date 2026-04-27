import os
import gzip
import pandas as pd
import numpy as np
import io
from utils.preprocessing import log_transform, normalize_data

def parse_geo_matrix(file_path):
    """
    Parses a GEO series matrix file to extract expression and survival metadata.
    """
    print(f"Parsing {file_path}...")
    
    metadata = {}
    expression_data_started = False
    expression_lines = []
    
    open_func = gzip.open if file_path.endswith('.gz') else open
    mode = 'rt' if file_path.endswith('.gz') else 'r'
    
    with open_func(file_path, mode) as f:
        for line in f:
            if line.startswith('!series_matrix_table_begin'):
                expression_data_started = True
                continue
            if line.startswith('!series_matrix_table_end'):
                break
            
            if not expression_data_started:
                if line.startswith('!Sample_title'):
                    metadata['Sample_title'] = line.strip().split('\t')[1:]
                elif line.startswith('!Sample_geo_accession'):
                    metadata['Sample_geo_accession'] = line.strip().split('\t')[1:]
                elif line.startswith('!Sample_characteristics_ch1'):
                    if 'characteristics' not in metadata:
                        metadata['characteristics'] = []
                    metadata['characteristics'].append(line.strip().split('\t')[1:])
            else:
                expression_lines.append(line)
    
    # Create Expression DF
    expr_df = pd.read_csv(io.StringIO("".join(expression_lines)), sep='\t', index_col=0)
    
    # Create Clinical DF from metadata
    clinical_data = {'sample': metadata['Sample_geo_accession']}
    
    # Try to find Survival Time and Event in characteristics
    # Note: GEO characteristics are messy and vary by series
    for char_list in metadata.get('characteristics', []):
        for i, val in enumerate(char_list):
            if ':' in val:
                key, value = val.split(':', 1)
                key = key.strip().lower()
                if key not in clinical_data:
                    clinical_data[key] = [None] * len(char_list)
                clinical_data[key][i] = value.strip()
    
    clinical_df = pd.DataFrame(clinical_data)
    clinical_df.set_index('sample', inplace=True)
    
    return expr_df, clinical_df

def align_and_save_geo(expr_df, clinical_df, name, ref_genes):
    """
    Aligns GEO data with reference genes and saves it.
    """
    print(f"Processing and Aligning {name}...")
    
    # Transpose expression: rows=samples, columns=probes/genes
    X = expr_df.T
    
    # Map probes to genes if necessary (simplified for now: assume index is gene symbols or handles later)
    # Most GEO matrix files have probes. We'll need a way to map them.
    # For now, we'll try to find common symbols.
    
    # Placeholder: Handle common GBM survival column names
    # Mapping common keys to 'OS.time' and 'OS'
    time_keys = ['survival time', 'os_days', 'os_months', 'survival (days)', 'overall survival (months)']
    status_keys = ['survival status', 'os_event', 'status', 'event', 'dead', 'vital status']
    
    found_time = None
    found_status = None
    
    for k in clinical_df.columns:
        for tk in time_keys:
            if tk in k:
                found_time = k
                break
        for sk in status_keys:
            if sk in k:
                found_status = k
                break
                
    if not found_time or not found_status:
        print(f"⚠️ Warning: Could not find survival columns in {name}. Columns: {clinical_df.columns.tolist()}")
        return
    
    # Clean up survival labels
    y = clinical_df[[found_time, found_status]].copy()
    y.columns = ['OS.time', 'OS']
    
    # Convert types
    y['OS.time'] = pd.to_numeric(y['OS.time'], errors='coerce')
    # Convert status to binary (0=alive, 1=dead)
    # This is highly dependent on the dataset's encoding
    y['OS'] = y['OS'].apply(lambda x: 1 if str(x).lower() in ['died', 'dead', '1', 'yes'] else 0)
    y = y.dropna()
    
    # Intersection
    common_samples = X.index.intersection(y.index)
    X = X.loc[common_samples]
    y = y.loc[common_samples]
    
    # Feature Alignment
    # (Omitted probe-to-gene mapping for now, will implement after inspecting files)
    
    processed_dir = f"data/processed/test_{name.lower()}"
    os.makedirs(processed_dir, exist_ok=True)
    
    # X.to_csv(os.path.join(processed_dir, "X.csv")) # Need mapping first
    y.to_csv(os.path.join(processed_dir, "y.csv"))
    print(f"✅ Partially processed {name} (Clinical data only for now).")

if __name__ == "__main__":
    # Example for GSE16011
    # ref_genes = pd.read_csv("data/processed/train/X.csv", nrows=0).columns[1:]
    pass
