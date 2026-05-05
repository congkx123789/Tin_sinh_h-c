import pandas as pd
import numpy as np
import requests
import os
import joblib
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.impute import KNNImputer
from sklearn.ensemble import IsolationForest

class RNASeqCleaner:
    def __init__(self, variance_threshold=0.01, expression_ratio=0.2):
        self.variance_threshold = variance_threshold
        self.expression_ratio = expression_ratio
        self.imputer = KNNImputer(n_neighbors=5)
        self.scaler = RobustScaler()
        self.iso_forest = IsolationForest(contamination=0.05, random_state=42)
        
    def fit_transform(self, df):
        print("--- Running Advanced RNA-Seq Cleaning Pipeline ---")
        
        # 1. Low-Expression & Variance Filtering
        print("1. Filtering low expression genes...")
        # Initial filter to reduce dimensionality before expensive imputation
        expr_mask = (df > 0).mean(axis=0) >= self.expression_ratio
        df_filtered = df.loc[:, expr_mask]
        
        variances = df_filtered.var()
        var_mask = variances > self.variance_threshold
        df_filtered = df_filtered.loc[:, var_mask]
        print(f"   Genes retained after initial filtering: {df_filtered.shape[1]} / {df.shape[1]}")
        
        # 2. Missing Value Imputation (on filtered genes only)
        print("2. Imputing missing values with KNN...")
        df_imputed = pd.DataFrame(self.imputer.fit_transform(df_filtered), columns=df_filtered.columns, index=df_filtered.index)
        self.features = df_filtered.columns.tolist()
            
        # 3. Outlier Detection (Isolation Forest)
        print("3. Detecting outlier patients...")
        outlier_preds = self.iso_forest.fit_predict(df_imputed)
        inlier_mask = outlier_preds == 1
        num_outliers = sum(~inlier_mask)
        print(f"   Detected and removed {num_outliers} outlier patients.")
        df_inliers = df_imputed[inlier_mask]
        
        # 4. Log1p Transformation
        print("4. Applying Log1p transformation...")
        df_log = np.log1p(df_inliers)
        
        # 5. Robust Scaling
        print("5. Applying Robust Scaling...")
        df_scaled = pd.DataFrame(
            self.scaler.fit_transform(df_log), 
            columns=df_log.columns, 
            index=df_log.index
        )
        
        self.features = df_log.columns.tolist()
        
        print("--- Pipeline Complete ---")
        return df_scaled, inlier_mask
        
    def transform(self, df):
        print("--- Running Transform Pipeline on Validation Data ---")
        if not hasattr(self, 'features'):
            raise ValueError("Cleaner not fitted. Load state first.")
            
        # 1. Align Features (CRITICAL)
        print(f"Aligning features to {len(self.features)} training genes...")
        df_aligned = df.reindex(columns=self.features, fill_value=0)
        
        # 2. Impute
        print("Imputing missing values...")
        if df_aligned.isna().sum().sum() > 0:
            # Use .values to bypass strict feature name checks
            df_imputed = pd.DataFrame(self.imputer.transform(df_aligned.values), columns=df_aligned.columns, index=df_aligned.index)
        else:
            df_imputed = df_aligned.copy()
            
        # 3. Log1p (Safe version)
        print("Applying Log1p (safe)...")
        # Ensure no negative values before log1p
        df_log = np.log1p(df_imputed.clip(lower=0))
        
        # 4. Robust Scaling (using fitted scaler)
        print("Applying Robust Scaling (fitted)...")
        df_scaled = pd.DataFrame(
            self.scaler.transform(df_log.values), 
            columns=df_log.columns, 
            index=df_log.index
        )
        return df_scaled
        
    def save_state(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        state = {
            'imputer': self.imputer,
            'scaler': self.scaler,
            'features': self.features
        }
        joblib.dump(state, path)
        print(f"✅ Cleaner state saved to {path}")
        
    def load_state(self, path):
        state = joblib.load(path)
        self.imputer = state['imputer']
        self.scaler = state['scaler']
        self.features = state['features']
        print(f"✅ Cleaner state loaded from {path}")

# Keep legacy functions for backward compatibility if needed
def filter_genes(df, variance_threshold=0.01):
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
