---
language: en
license: mit
task_categories:
- tabular-classification
- feature-extraction
tags:
- bioinformatics
- cancer-research
- glioblastoma
- survival-prediction
- gene-expression
pretty_name: GBM Survival Gene Expression Dataset
size_categories:
- 1GB<n<10GB
---

# 🧬 GBM Survival Gene Expression Dataset

This dataset contains large-scale gene expression data (RNA-Seq and Microarray) curated for predicting the survival outcomes of patients with Glioblastoma Multiforme (GBM) and Lower-Grade Glioma (LGG).

It is specifically designed to be used with the [GBM Survival LightGBM](https://github.com/congkx123789/Tin_sinh_h-c) project.

## 📂 Data Structure

The data is organized into three main phases:

### 1. `01_raw/` (Raw Data)
Untouched genomic data from international portals:
- **TCGA**: RNA-Seq data from The Cancer Genome Atlas (USA).
- **CGGA**: Chinese Glioma Genome Atlas data (Asia).
- **GEO**: Various cohorts from NCBI Gene Expression Omnibus (REMBRANDT, GSE4412, etc.).

### 2. `02_processed/` (Cleaned & Normalized)
Ready-to-use data for machine learning:
- **training/**: Internal Train/Val/Test splits used for model development.
- **validation/**: External independent cohorts for performance verification.
- Files include `X.csv` (feature matrices with 16,383 genes) and `y.csv` (survival time and status).

### 3. `03_metadata/`
Mapping tables between Gene Symbols and Probe IDs, as well as clinical metadata.

## 🚀 How to use with the Project

If you have cloned the [GitHub repository](https://github.com/congkx123789/Tin_sinh_h-c), you can automatically sync this data by running:

```bash
python scripts/download_data_hf.py
```

This will download all files and place them in the correct `data/` directory structure.

## 📝 Data Sources & Citations

If you use this data, please cite the original sources:
1. TCGA Research Network: https://www.cancer.gov/tcga
2. CGGA Database: http://www.cgga.org.cn/
3. NCBI GEO: https://www.ncbi.nlm.nih.gov/geo/

**Project Maintainer**: Cong, K. X.
