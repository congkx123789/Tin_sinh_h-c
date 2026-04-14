import pandas as pd
import numpy as np
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
    return pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
