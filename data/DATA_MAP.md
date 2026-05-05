# 🗺️ Bản đồ Cấu trúc Dữ liệu (Data Structure Map)

Dự án này sử dụng dữ liệu biểu hiện gen từ nhiều nguồn quốc tế. Để đảm bảo tính nhẹ nhàng và tuân thủ các quy định về dữ liệu lớn, thư mục `data/` được lưu trữ trên **Hugging Face Hub**.

## 🔄 Đồng bộ Dữ liệu Tự động (Khuyên dùng)

Cách nhanh nhất để chuẩn bị dữ liệu là sử dụng script đồng bộ:
```bash
python scripts/download_data_hf.py
```

## 📂 Sơ đồ tổ chức thư mục yêu cầu (Required Structure)

Nếu bạn muốn chạy dự án này, hãy đảm bảo dữ liệu được đặt đúng vị trí sau:

```text
data/
├── 01_raw/                 # Dữ liệu gốc (Raw Data)
│   ├── TCGA/               # File lgg_rna_seq.tsv.gz, v.v.
│   ├── CGGA/               # Các file từ cgga.org.cn
│   └── GEO/                # REMBRANDT_matrix.gz, v.v.
├── 02_processed/           # Dữ liệu đã chuẩn hóa (X.csv, y.csv)
│   ├── training/           # Dữ liệu cho Train/Val/Test
│   └── validation/         # Thư mục cho CGGA_325, CGGA_693, REMBRANDT, TCGA_LGG...
└── 03_metadata/            # Bảng ánh xạ gen và ID probe
```

## 📋 Danh sách các bộ dữ liệu chính

1.  **TCGA-GBM & TCGA-LGG**: Dữ liệu RNA-seq từ GDC Portal.
2.  **CGGA (325 & 693 samples)**: Dữ liệu từ Chinese Glioma Genome Atlas.
3.  **GEO Cohorts**: Bao gồm REMBRANDT, GSE4412, GSE13041, GSE4271, GSE7696.

## ⚙️ Quy trình xử lý dữ liệu

Mã nguồn trong thư mục `scripts/` cung cấp đầy đủ các bước để tái lập dữ liệu:

1.  **Tiền xử lý**: Sử dụng `preprocess_data.py` để lọc gen và chuẩn hóa log-transform.
2.  **Đồng bộ**: `sync_validation_data.py` giúp đảm bảo các bộ dữ liệu kiểm chứng có cùng danh sách gen với bộ huấn luyện.
3.  **Tạo báo cáo**: `patient_gene_report.py` có thể được sử dụng để kiểm tra dữ liệu của từng mẫu bệnh nhân cụ thể.

---
**Lưu ý**: Các file trọng số mô hình trong `checkpoints/` đã được huấn luyện trên 16,504 gen phổ biến nhất trong u não. Dữ liệu đầu vào mới cần được ánh xạ đúng danh sách gen này để mô hình hoạt động chính xác.
