# 🧬 GBM Survival Prediction using Mamba-SSM

Mô hình học sâu tiên tiến sử dụng kiến trúc **Mamba (Selective State Space Model)** để dự đoán tiên lượng sống sót của bệnh nhân Ung thư não (Glioblastoma Multiforme - GBM) dựa trên dữ liệu biểu hiện gen (RNA-Seq) từ dự án TCGA.

## 🎯 Mục tiêu dự án

Mục tiêu chính của dự án là giải quyết bài toán "Số lượng gen cực lớn nhưng ít mẫu bệnh nhân" (The $p \gg n$ problem) trong sinh tin học bằng cách:
1.  **Nén dữ liệu**: Sử dụng **Denoising Autoencoder (DAE)** để cô đặc 16,504 gen xuống một không gian tiềm ẩn (Latent space) 128 chiều, giúp loại bỏ nhiễu sinh học.
2.  **Mô hình hóa chuỗi**: Sử dụng **Mamba** - một kiến trúc mới mạnh mẽ hơn cả Transformer đối với các chuỗi dài - để học các tương tác phức tạp giữa các cụm đặc trưng gen.
3.  **Phân tầng rủi ro**: Cung cấp một chỉ số rủi ro (Risk Score) giúp bác sĩ tiên lượng được mức độ hung hãn của khối u, hỗ trợ quyết định phác đồ điều trị.

## 🏗 Cấu trúc mã nguồn (Code Structure)

```text
gbm_survival_mamba/
├── data/
│   ├── raw/               # Chứa dữ liệu gốc từ TCGA (rna_seq, clinical, survival)
│   └── processed/         # Dữ liệu sau khi giải mã Gen Symbol và chia tập (Train/Val/Test)
├── models/
│   ├── autoencoder.py      # Kiến trúc Denoising Autoencoder (DAE)
│   ├── mamba_block.py      # Khối Mamba-SSM (hỗ trợ placeholder nếu thiếu CUDA)
│   └── survival_net.py     # Mô hình tích hợp (DAE Encoder + Mamba + Survival Head)
├── scripts/
│   ├── setup_data.py       # Tự động tải dữ liệu từ UCSC Xena Hub
│   ├── preprocess_data.py  # Làm sạch, giải mã gen (API MyGene.info) và chia Stratified Split
│   ├── train_ae.py         # Huấn luyện unsupervised cho Autoencoder
│   ├── train_mamba.py      # Huấn luyện supervised với Cox Partial Likelihood Loss
│   └── evaluate.py         # Đánh giá mô hình (C-index) và vẽ biểu đồ Kaplan-Meier
├── utils/
│   ├── data_loader.py      # Xử lý nạp dữ liệu cho PyTorch
│   ├── preprocessing.py    # Các hàm bổ trợ (log2 transform, normalization, API mapping)
│   ├── loss.py             # Cài đặt hàm Cox Loss (Log Partial Likelihood)
│   └── metrics.py          # Tính toán C-index và Kaplan-Meier (thuật toán gốc)
├── results/                # Lưu trữ kết quả đồ thị (KM Plot)
├── checkpoints/            # Lưu trữ trọng số mô hình tốt nhất (.pth)
├── requirements.txt        # Danh sách thư viện cần thiết
└── run.py                  # Script chạy nhanh toàn bộ pipeline
```

## 🛠 Hướng dẫn sử dụng

### 1. Cài đặt môi trường
```bash
pip install -r requirements.txt
```

### 2. Tiền xử lý dữ liệu
Quy trình này sẽ tự động tải dữ liệu, giải mã Ensembl ID sang Gene Symbol và chia tập dữ liệu 70-15-15:
```bash
python scripts/preprocess_data.py
```

### 3. Huấn luyện (2 bước)
**Bước 1: Huấn luyện bộ nén đặc trưng (Pre-train AE)**
```bash
python scripts/train_ae.py
```
**Bước 2: Huấn luyện mô hình sinh tồn chính (Mamba)**
```bash
python scripts/train_mamba.py
```

### 4. Đánh giá kết quả
```bash
python scripts/evaluate.py
```

## 📊 Kết quả đạt được

Hệ thống hiện tại đạt được hiệu suất như sau trên tập dữ liệu Test độc lập:

*   **Chỉ số Concordance (C-index)**: **0.6151**
*   **Phân tầng rủi ro**: Mô hình phân loại thành công 2 nhóm bệnh nhân (Nguy cơ Cao vs Nguy cơ Thấp) với sự khác biệt rõ rệt về thời gian sống sót trên biểu đồ Kaplan-Meier.

---
**Dự án được phát triển nhằm mục đích nghiên cứu Tin sinh học và Hỗ trợ y học số.**
