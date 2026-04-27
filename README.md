# 🧬 GBM Survival Prediction using Mamba-SSM

Mô hình học sâu sử dụng kiến trúc **Mamba (Selective State Space Model)** để dự đoán tiên lượng sống sót của bệnh nhân u não (GBM) từ dữ liệu biểu hiện gen (16,504 gen).

## 🚀 Hướng dẫn bắt đầu nhanh (Quick Start)

### 1. Cài đặt môi trường
```bash
conda create -n mamba_env python=3.10
conda activate mamba_env
pip install -r requirements.txt
```

### 2. Khôi phục dữ liệu (Bắt buộc nếu tải từ GitHub)
Do giới hạn 100MB của GitHub, dữ liệu lớn được chia nhỏ. Chạy script sau để khôi phục:
```bash
bash scripts/reconstruct_data.sh
```

### 3. Đánh giá mô hình
Sử dụng mô hình đã huấn luyện để kiểm chứng trên các tập dữ liệu:
```bash
python scripts/evaluate.py [split_name]
# Ví dụ: python scripts/evaluate.py test_cgga_325
```

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

## 📂 Cấu trúc Dự án
```text
data/
├── 01_raw/          # Dữ liệu gốc quốc tế
├── 02_processed/    # Dữ liệu sạch cho Training/Validation
└── 03_metadata/     # Bảng ánh xạ gen
scripts/             # Pipeline xử lý & Đánh giá
models/              # Kiến trúc Mamba & Autoencoder
results/             # Biểu đồ Kaplan-Meier
```

## 🌐 Nguồn dữ liệu (Data Sources)
Chi tiết xem tại [data/DATA_MAP.md](./data/DATA_MAP.md).

---
**Project phát triển bởi AI Agent & Chuyên gia.**
