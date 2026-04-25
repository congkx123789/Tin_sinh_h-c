import pandas as pd
import numpy as np
import requests
from sklearn.preprocessing import StandardScaler

def filter_genes(df, variance_threshold=0.01):
    # Filter genes with low variance
    variances = df.var()
    selected_genes = variances[variances > variance_threshold].index
    return df[selected_genes]

def log_transform(df):
    return np.log1p(df)

def normalize_data(df):
    scaler = StandardScaler()
    return pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)

def fetch_gene_symbols(ensembl_ids):
    """
    Fetch gene symbols from MyGene.info API
    """
    print(f"Fetching mapping for {len(ensembl_ids)} genes via MyGene.info...")
    
    # Strip versions if present (e.g. ENSGxxx.13 -> ENSGxxx)
    base_ids = [str(gid).split('.')[0] for gid in ensembl_ids]
    
    url = "https://mygene.info/v3/query"
    chunk_size = 1000
    mapping_dict = {}
    
    for i in range(0, len(base_ids), chunk_size):
        chunk = base_ids[i:i + chunk_size]
        payload = {
            'q': chunk,
            'scopes': 'ensembl.gene',
            'fields': 'symbol',
            'species': 'human'
        }
        try:
            response = requests.post(url, json=payload)
            results = response.json()
            for item in results:
                if 'symbol' in item:
                    mapping_dict[item['query']] = item['symbol']
            
            # Progress update
            print(f"Mapped {min(i + chunk_size, len(base_ids))}/{len(base_ids)} genes...")
        except Exception as e:
            print(f"Error fetching symbols: {e}")
            
    return mapping_dict

def map_ensembl_to_symbol(rna_df, mapping_df=None):
    """
    rna_df: Columns are genes (Ensembl IDs), Rows are patients
    mapping_df: (Optional) Pre-loaded DataFrame with 'id' and 'gene'
    """
    ensembl_ids = rna_df.columns.tolist()
    
    if mapping_df is not None and not mapping_df.empty and 'id' in mapping_df.columns:
        print("Using provided mapping file...")
        mapping_dict = dict(zip(mapping_df['id'], mapping_df['gene']))
    else:
        print("Mapping file missing or invalid. Falling back to MyGene.info API...")
        mapping_dict = fetch_gene_symbols(ensembl_ids)
    
    # Map current columns (Ensembl IDs) to symbols
    # We try mapping both full ID and base ID
    new_columns = []
    for cid in rna_df.columns:
        base_id = str(cid).split('.')[0]
        symbol = mapping_dict.get(cid) or mapping_dict.get(base_id) or cid
        new_columns.append(symbol)
        
    rna_df.columns = new_columns
    
    # Filter out columns that were NOT mapped to human-readable symbols 
    # (Keep only columns that don't start with ENSG)
    mappable_cols = [c for c in rna_df.columns if not str(c).startswith('ENSG')]
    print(f"Mapped {len(mappable_cols)} out of {len(rna_df.columns)} IDs")
    
    if len(mappable_cols) == 0:
        print("WARNING: No columns were mapped to Gene Symbols!")
        return rna_df
        
    rna_df = rna_df[mappable_cols]
    
    # Aggregate duplicate gene symbols (mean)
    rna_df = rna_df.groupby(axis=1, level=0).mean()
    
    return rna_df
