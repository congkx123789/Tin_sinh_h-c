# 🗺️ Bản đồ Cấu trúc Dữ liệu (Data Structure Map)

Tài liệu này hướng dẫn chi tiết cách tổ chức dữ liệu trong dự án và cách khôi phục các tệp tin lớn đã bị chia nhỏ để vượt qua giới hạn 100MB của GitHub.

## 📂 Sơ đồ tổ chức thư mục (Directory Tree)

```text
data/
├── 01_raw/                 # Dữ liệu gốc từ nguồn (Raw Data)
│   ├── TCGA/               # Nguồn TCGA-GBM/LGG
│   ├── CGGA/               # Nguồn Chinese Glioma Genome Atlas
│   └── GEO/                # Nguồn NCBI Gene Expression Omnibus
├── 02_processed/           # Dữ liệu đã làm sạch & Chuẩn hóa
│   ├── training/           # Dữ liệu cho Train/Val/Test nội bộ
│   └── validation/         # Các quần thể kiểm chứng độc lập
└── 03_metadata/            # Bảng ánh xạ gen và ID probe
```

## 📦 Danh sách các tệp tin lớn đã chia nhỏ (Split Files)

Dưới đây là bảng tra cứu để khôi phục các tệp tin gốc nếu bạn tải dự án từ GitHub:

| Tên file gốc (Original) | Các phần trên GitHub (Parts) | Thư mục chứa |
| :--- | :--- | :--- |
| `REMBRANDT_matrix.gz` | `.part-aa`, `.part-ab` | `data/01_raw/GEO/` |
| `lgg_rna_seq.tsv.gz` | `.part-aa`, `.part-ab` | `data/01_raw/TCGA/` |
| `lgg_rna_seq_test.tsv.gz` | `.part-aa`, `.part-ab` | `data/01_raw/TCGA/` |
| `X.csv` (CGGA-693) | `.part-aa` -> `.part-ac` | `data/02_processed/validation/CGGA_693/` |
| `X.csv` (REMBRANDT) | `.part-aa`, `.part-ab` | `data/02_processed/validation/REMBRANDT/` |
| `X.csv` (TCGA-LGG) | `.part-aa` -> `.part-ac` | `data/02_processed/validation/TCGA_LGG/` |

## 🛠️ Hướng dẫn khôi phục dữ liệu (Reconstruction)

Để khôi phục toàn bộ dữ liệu về trạng thái ban đầu sau khi `git clone`, hãy chạy lệnh sau tại thư mục gốc của dự án:

```bash
# 1. Khôi phục dữ liệu thô GEO
cat data/01_raw/GEO/REMBRANDT_matrix.gz.part-* > data/01_raw/GEO/REMBRANDT_matrix.gz

# 2. Khôi phục dữ liệu thô TCGA
cat data/01_raw/TCGA/lgg_rna_seq.tsv.gz.part-* > data/01_raw/TCGA/lgg_rna_seq.tsv.gz
cat data/01_raw/TCGA/lgg_rna_seq_test.tsv.gz.part-* > data/01_raw/TCGA/lgg_rna_seq_test.tsv.gz

# 3. Khôi phục dữ liệu đã xử lý (X.csv)
cat data/02_processed/validation/CGGA_693/X.csv.part-* > data/02_processed/validation/CGGA_693/X.csv
cat data/02_processed/validation/REMBRANDT/X.csv.part-* > data/02_processed/validation/REMBRANDT/X.csv
cat data/02_processed/validation/TCGA_LGG/X.csv.part-* > data/02_processed/validation/TCGA_LGG/X.csv

# Lưu ý: Sau khi khôi phục, bạn có thể xóa các file .part-* để tiết kiệm dung lượng.
```

---
**Tài liệu này giúp đảm bảo tính toàn vẹn của dữ liệu trong quá trình validation.**
