# 🧬 GBM Survival Prediction using Mamba-SSM

Mô hình học sâu tiên tiến sử dụng kiến trúc **Mamba (Selective State Space Model)** kết hợp với **Denoising Autoencoder (DAE)** để dự đoán tiên lượng sống sót của bệnh nhân u não (Glioblastoma) dựa trên dữ liệu biểu hiện gen.

## 🚀 Hướng dẫn bắt đầu (Quick Start)

### 1. Cài đặt môi trường
Dự án yêu cầu Python 3.10+ và các thư viện trong `requirements.txt`.
```bash
conda create -n mamba_env python=3.10
conda activate mamba_env
pip install -r requirements.txt
# Lưu ý: Cần cài đặt mamba-ssm từ https://github.com/state-spaces/mamba
```

### 2. Cấu trúc dữ liệu
Thư mục `data/` hiện tại được để trống trên GitHub để giữ repository nhẹ. Bạn cần chuẩn bị dữ liệu theo cấu trúc sau:
- `data/01_raw/`: Chứa các file TSV/CSV gốc từ TCGA, CGGA, GEO.
- `data/02_processed/`: Chứa dữ liệu đã qua tiền xử lý (X.csv, y.csv).

*Xem chi tiết tại [data/DATA_MAP.md](./data/DATA_MAP.md).*

### 3. Sử dụng mô hình đã huấn luyện
Sử dụng các trọng số trong `checkpoints/` để dự đoán hoặc đánh giá:
```bash
# Đánh giá trên tập dữ liệu cụ thể
python scripts/evaluate.py [split_name]

# Dự đoán cho một bệnh nhân cụ thể (custom data)
python scripts/test_custom_patient.py --input path/to/patient_data.csv
```

## 📊 Các công cụ phân tích (Scripts)

Dự án cung cấp bộ công cụ mạnh mẽ để phân tích và báo cáo:

- **Dự đoán & Báo cáo**:
    - `patient_gene_report.py`: Tạo báo cáo chi tiết về biểu hiện gen và mức độ nguy cơ cho từng bệnh nhân.
    - `predict_condition.py`: Dự đoán tình trạng bệnh dựa trên biểu hiện gen.
- **Trực quan hóa**:
    - `visualize_classifier.py`: Vẽ biểu đồ phân loại và ma trận nhầm lẫn.
    - `visualize_biomarker_landscape.py`: Trực quan hóa bản đồ các dấu ấn sinh học (biomarkers).
- **Phân tích Dấu ấn sinh học**:
    - `extract_global_biomarkers.py`: Tìm ra các gen có ảnh hưởng lớn nhất đến tiên lượng sống sót.
    - `analyze_treatment.py`: Phân tích mối liên hệ giữa điều trị và biểu hiện gen.

## 🎯 Kết quả Thực nghiệm (C-index)

Mô hình đạt kết quả ổn định trên nhiều quần thể kiểm chứng độc lập:

| Nguồn dữ liệu | Số mẫu | Nền tảng | C-index |
| :--- | :--- | :--- | :--- |
| **TCGA-GBM** (Internal) | 150+ | RNA-Seq | **0.6151** |
| **TCGA-LGG** (External) | 500+ | RNA-Seq | **0.6569** |
| **CGGA-325** | 325 | RNA-Seq | **0.6325** |
| **CGGA-693** | 693 | RNA-Seq | **0.5793** |

## 📂 Sơ đồ tổ chức (Architecture)
```text
├── checkpoints/      # Trọng số mô hình (DAE & Mamba)
├── models/           # Định nghĩa kiến trúc (Mamba, Autoencoder, SurvivalNet)
├── scripts/          # Scripts huấn luyện, tiền xử lý và phân tích
├── utils/            # Các hàm bổ trợ xử lý dữ liệu
└── results/          # Kết quả đầu ra (Biểu đồ, CSV báo cáo)
```
