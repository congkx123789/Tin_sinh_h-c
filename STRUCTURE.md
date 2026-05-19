# 📂 Cấu trúc dự án GBM Survival LightGBM

Tài liệu này trình bày cấu trúc tệp tin của dự án **GBM Survival LightGBM**.

```text
gbm_survival_lightgbm/
├── 📁 data/                  # Dữ liệu RNA-Seq và Clinical
│   ├── 📁 01_raw/            # Dữ liệu thô từ TCGA/CGGA
│   ├── 📁 02_processed/      # Dữ liệu đã qua tiền xử lý
│   └── 📁 03_metadata/       # Mapping gen và thông tin bổ sung
├── 📁 models/                # Định nghĩa các mô hình
│   └── 📄 autoencoder.py      # Denoising Autoencoder (DAE)
├── 📁 scripts/               # Các luồng xử lý chính
│   ├── 📄 preprocess_data.py  # Tiền xử lý & lọc gen
│   ├── 📄 train_ae.py        # Huấn luyện Autoencoder
│   ├── 📄 train_lightgbm.py   # Huấn luyện mô hình LightGBM
│   └── 📄 evaluate.py        # Đánh giá & Kaplan-Meier
├── 📁 checkpoints/           # Lưu trữ trọng số mô hình
│   ├── 📁 ae_weights/
│   └── 📁 lightgbm_weights/
├── 📁 results/               # Kết quả trực quan hóa (KM plots)
├── 📄 run.py                 # File thực thi chính
├── 📄 config.yaml            # Cấu hình tham số
└── 📄 requirements.txt       # Các thư viện cần thiết
```
