import pandas as pd
import os

def inspect_cgga():
    expr_path = "data/raw/cgga/CGGA.mRNAseq_693.RSEM-genes.20200506.txt"
    clinical_path = "data/raw/cgga/CGGA.mRNAseq_693_clinical.20200506.txt"
    
    print("--- Expression Data ---")
    expr_df = pd.read_csv(expr_path, sep='\t', nrows=5)
    print("Columns:", expr_df.columns.tolist()[:10], "... total:", len(expr_df.columns))
    print("First few rows:")
    print(expr_df.iloc[:, :5])
    
    print("\n--- Clinical Data ---")
    clinical_df = pd.read_csv(clinical_path, sep='\t')
    print("Columns:", clinical_df.columns.tolist())
    print("Shape:", clinical_df.shape)
    print("First 5 rows:")
    print(clinical_df[['CGGA_ID', 'OS', 'Censor (alive=0; dead=1)']].head())

if __name__ == "__main__":
    inspect_cgga()
