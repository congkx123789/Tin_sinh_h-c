# 🧬 GBM Survival Prediction using Mamba-SSM

Mô hình học sâu tiên tiến sử dụng kiến trúc **Mamba (Selective State Space Model)** để dự đoán tiên lượng sống sót của bệnh nhân Ung thư não (Glioblastoma Multiforme - GBM) dựa trên dữ liệu biểu hiện gen (RNA-Seq) từ dự án TCGA.

## 🎯 Mục tiêu dự án

Mục tiêu chính của dự án là giải quyết bài toán "Số lượng gen cực lớn nhưng ít mẫu bệnh nhân" (The $p \gg n$ problem) trong sinh tin học bằng cách:
1.  **Nén dữ liệu**: Sử dụng **Denoising Autoencoder (DAE)** để cô đặc 16,504 gen xuống một không gian tiềm ẩn (Latent space) 128 chiều, giúp loại bỏ nhiễu sinh học.
2.  **Mô hình hóa chuỗi**: Sử dụng **Mamba** - một kiến trúc mới mạnh mẽ hơn cả Transformer đối với các chuỗi dài - để học các tương tác phức tạp giữa các cụm đặc trưng gen.
3.  **Phân tầng rủi ro**: Cung cấp một chỉ số rủi ro (Risk Score) giúp bác sĩ tiên lượng được mức độ hung hãn của khối u, hỗ trợ quyết định phác đồ điều trị.

## 🕒 Nhật ký Quy trình thực hiện (Step-by-Step)

1.  **Bước 1: Thu thập Dữ liệu thô**: Tải RNA-Seq và Survival data từ TCGA-GBM. Xử lý lỗi file mapping bằng cách dùng **MyGene.info API**.
2.  **Bước 2: Tiền xử lý Sinh tin học**: Thực hiện Log2 transform, Z-score normalization và lọc ra **16,504 gen** biến thiên cao nhất.
3.  **Bước 3: Nén đặc trưng (DAE)**: Huấn luyện Autoencoder để nén dữ liệu xuống **128 chiều** tiềm ẩn.
4.  **Bước 4: Kiến trúc Mamba-SSM**: Băm chuỗi 128-dim thành **8 token (16-dim)** để tận dụng sức mạnh Selective State Space của Mamba.
5.  **Bước 5: Huấn luyện & Tổ chức**: Dùng Cox Loss, chia dữ liệu **Stratified Split** và tự động hóa việc phân chia vào các thư mục `train/val/test`.
6.  **Bước 6: Kiểm chứng ngoại kiểm**: Đang thực hiện đánh giá độ tổng quát trên tập dữ liệu **TCGA-LGG**.

## 🏗 Cấu trúc mã nguồn (Code Structure)

```text
gbm_survival_mamba/
├── data/
│   ├── raw/               # Dữ liệu gốc từ TCGA (.tsv.gz)
│   └── processed/         # Dữ liệu sạch đã chia folder
│       ├── train/         # Dữ liệu huấn luyện (GBM)
│       ├── val/           # Dữ liệu kiểm chứng
│       ├── test_internal/ # Dữ liệu test nội bộ (GBM)
│       └── test_lgg/      # Dữ liệu test ngoại kiểm (LGG)
├── models/                # Autoencoder.py, mamba_block.py, survival_net.py
├── scripts/               # Các script chạy pipeline (Preprocess, Train, Evaluate)
├── utils/                 # Metrics, API Mapping, Loss function
├── results/               # Chứa các biểu đồ Kaplan-Meier (.png)
├── checkpoints/           # Lưu trữ trọng số mô hình (.pth)
└── requirements.txt       # Thư viện cần thiết
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
