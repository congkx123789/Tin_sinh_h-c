#!/bin/bash

echo "🚀 Starting Data Reconstruction..."

# Function to reconstruct split files
reconstruct() {
    local target=$1
    local part_prefix=$2
    if ls ${part_prefix}* 1> /dev/null 2>&1; then
        echo "📦 Reconstructing $target..."
        cat ${part_prefix}* > "$target"
        echo "✅ Created $target"
    else
        echo "ℹ️ No parts found for $target, skipping."
    fi
}

# 1. Raw Data GEO
reconstruct "data/01_raw/GEO/REMBRANDT_matrix.gz" "data/01_raw/GEO/REMBRANDT_matrix.gz.part-"

# 2. Raw Data TCGA
reconstruct "data/01_raw/TCGA/lgg_rna_seq.tsv.gz" "data/01_raw/TCGA/lgg_rna_seq.tsv.gz.part-"
reconstruct "data/01_raw/TCGA/lgg_rna_seq_test.tsv.gz" "data/01_raw/TCGA/lgg_rna_seq_test.tsv.gz.part-"

# 3. Processed Validation Data
reconstruct "data/02_processed/validation/CGGA_693/X.csv" "data/02_processed/validation/CGGA_693/X.csv.part-"
reconstruct "data/02_processed/validation/REMBRANDT/X.csv" "data/02_processed/validation/REMBRANDT/X.csv.part-"
reconstruct "data/02_processed/validation/TCGA_LGG/X.csv" "data/02_processed/validation/TCGA_LGG/X.csv.part-"

echo "✨ All large files have been reconstructed successfully!"
echo "💡 You can now delete the .part-* files if you want to save disk space."
