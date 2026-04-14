import os
import pandas as pd
from utils.preprocessing import filter_genes, log_transform, normalize_data

def main():
    print("Preprocessing data...")
    # Paths (should ideally be loaded from config)
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
        
    # Example logic
    # rna_seq = pd.read_csv(os.path.join(raw_dir, "RNA_Seq.tsv"), sep='\t')
    # clinical = pd.read_csv(os.path.join(raw_dir, "Clinical.csv"))
    
    # processed_rna = normalize_data(log_transform(filter_genes(rna_seq)))
    # processed_rna.to_csv(os.path.join(processed_dir, "processed_rna.csv"), index=False)
    
    print("Preprocessing complete (placeholder).")

if __name__ == "__main__":
    main()
