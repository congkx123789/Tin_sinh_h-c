# 🧬 GBM Survival Prediction using Mamba-SSM

Mô hình học sâu sử dụng kiến trúc **Mamba (Selective State Space Model)** để dự đoán tiên lượng sống sót của bệnh nhân u u não (GBM) từ dữ liệu biểu hiện gen (16,504 gen).

## 🎯 Kết quả Kiểm chứng (C-index)

| Nguồn dữ liệu | Nền tảng | Số mẫu | C-index |
| :--- | :--- | :--- | :--- |
| **TCGA-GBM** (Internal) | RNA-Seq | 150+ | **0.6151** |
| **TCGA-LGG** (External) | RNA-Seq | 500+ | **0.6569** 🚀 |
| **CGGA-325** | RNA-Seq | 325 | **0.6325** |
| **CGGA-693** | RNA-Seq | 693 | **0.5793** |
| **GSE4412** | Microarray | 85 | **0.5801** |
| **GSE13041** | Microarray | 191 | **0.5478** |
| **REMBRANDT** | Microarray | 490 | **0.4582** |

## 📂 Cấu trúc Dữ liệu
```text
data/
├── 01_raw/          # Dữ liệu gốc (TCGA, CGGA, GEO)
├── 02_processed/    # Dữ liệu sạch (Training & Validation)
└── 03_metadata/     # Bảng ánh xạ Gen & ID
```

## 🚀 Cách chạy nhanh
1. **Huấn luyện**: `python scripts/train_ae.py` & `python scripts/train_mamba.py`
2. **Đánh giá**: `python scripts/evaluate.py [split_name]`

## 📦 Cách khôi phục dữ liệu lớn (Reconstructing Large Files)
Do giới hạn 100MB của GitHub, các tệp >100MB đã được chia nhỏ (`.part-aa`, `.part-ab`). Để khôi phục, hãy chạy:
```bash
cat data/01_raw/GEO/REMBRANDT_matrix.gz.part-* > data/01_raw/GEO/REMBRANDT_matrix.gz
cat data/01_raw/TCGA/lgg_rna_seq.tsv.gz.part-* > data/01_raw/TCGA/lgg_rna_seq.tsv.gz
cat data/02_processed/validation/CGGA_693/X.csv.part-* > data/02_processed/validation/CGGA_693/X.csv
# Tương tự cho các file .part khác
```

## 🌐 Nguồn dữ liệu (Data Sources)
1. **TCGA**: [GDC Portal](https://portal.gdc.cancer.gov/)
2. **CGGA**: [CGGA Website](http://www.cgga.org.cn/)
3. **GEO**: [GSE108476](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE108476), [GSE4271](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4271), [GSE7696](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE7696), [GSE13041](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE13041), [GSE4412](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4412)

---
**Project phát triển bởi AI Agent & Chuyên gia.**
