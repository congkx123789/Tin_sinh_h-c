# 🧬 GBM Survival Mamba: Advanced Prognosis using Hybrid DAE-Mamba

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Dự án này triển khai một hệ thống AI tiên tiến nhằm dự đoán tiên lượng sống sót cho bệnh nhân Ung thư não (Glioblastoma Multiforme - GBM). Đây là sự kết hợp đột phá giữa **Denoising Autoencoder (DAE)** và **Mamba (Selective State Space Model)** để xử lý dữ liệu biểu hiện gen đa chiều.

---

## 🌟 Tính năng Nổi bật (Key Features)

*   **Dự đoán Tiên lượng Chính xác (Precision Prognosis)**: Tính toán chỉ số rủi ro (Risk Score) cá thể hóa với độ tin cậy cao trên nhiều quần thể kiểm chứng.
*   **Giải thích mô hình (Explainable AI - XAI)**: Trích xuất các "Dấu ấn sinh học" (Biomarkers) có ảnh hưởng lớn nhất đến kết quả sống sót thông qua cơ chế tính toán Gradient.
*   **Khả năng tương thích đa nền tảng**: Xử lý mượt mà cả dữ liệu **RNA-Seq** và **Microarray** nhờ quy trình tiền xử lý đồng bộ 16,383 gen.
*   **Hệ thống Báo cáo Phân tử**: Tự động tạo báo cáo chi tiết cho từng bệnh nhân (`patient_gene_report.py`).

---

## 🏗️ Kiến trúc Kỹ thuật (Architecture & Innovations)

Dự án áp dụng mô hình Hybrid tiên tiến nhất hiện nay trong lĩnh vực Tin sinh học:

### 1. Denoising Autoencoder (DAE) - Bộ lọc Nhiễu Sinh học
Trước khi đưa vào mô hình chính, dữ liệu biểu hiện gen thô được đưa qua một bộ **Autoencoder**. Bước này giúp nén 16,383 đặc trưng xuống còn 128 chiều latent, đồng thời loại bỏ các nhiễu đo lường thường gặp trong dữ liệu sinh học.

### 2. Mamba-SSM: Cuộc cách mạng trong học chuỗi gen
Thay vì sử dụng MLP đơn thuần, chúng tôi áp dụng kiến trúc **Mamba**. Điểm cải tiến nằm ở việc **Token hóa không gian Latent**:
*   Vector 128 chiều được chia thành một chuỗi gồm 8 tokens.
*   Lớp Mamba học các mối quan hệ phi tuyến phức tạp giữa các cụm đặc trưng này, tương tự như cách Transformer xử lý ngôn ngữ nhưng với hiệu suất cao hơn và khả năng bắt lấy các phụ thuộc xa tốt hơn.

### 3. Phân tích Dấu ấn Sinh học (Global & Local Biomarkers)
Sử dụng phương pháp **Integrated Gradients** để xác định:
*   **Malignant Genes**: Các gen làm tăng nguy cơ tử vong khi biểu hiện cao.
*   **Protective Genes**: Các gen bảo vệ, giúp kéo dài thời gian sống.

---

## 🚀 Hướng dẫn Cài đặt & Sử dụng

### Cài đặt môi trường
```bash
conda create -n mamba_env python=3.10
conda activate mamba_env
pip install -r requirements.txt
# Lưu ý: Yêu cầu cài đặt thư viện mamba-ssm từ nguồn chính thức
```

### Sử dụng mô hình đã huấn luyện
Toàn bộ trọng số tốt nhất đã được lưu trong thư mục `checkpoints/`. Bạn có thể sử dụng ngay để dự đoán:
```bash
# Đánh giá trên các bộ validation (CGGA, REMBRANDT, v.v.)
python scripts/evaluate.py test_cgga_325

# Trực quan hóa kết quả phân loại
python scripts/visualize_classifier.py
```

---

## 📂 Danh mục Công cụ (Analysis Tools)

| Script | Công dụng |
| :--- | :--- |
| `patient_gene_report.py` | Tạo báo cáo chi tiết cấp độ bệnh nhân |
| `extract_global_biomarkers.py` | Tìm kiếm các gen chủ chốt ảnh hưởng đến tiên lượng |
| `visualize_biomarker_landscape.py` | Bản đồ nhiệt (Heatmap) về các dấu ấn sinh học |
| `predict_condition.py` | Dự đoán tình trạng bệnh nhân dựa trên mẫu gen |

---

## 🎯 Kết quả Thực nghiệm (Benchmarks)

Hệ thống đã được kiểm chứng trên các quần thể độc lập với chỉ số C-index ổn định:

| Dataset | Type | Samples | C-index |
| :--- | :--- | :--- | :--- |
| **TCGA-GBM** | RNA-Seq | 150+ | **0.6151** |
| **TCGA-LGG** | RNA-Seq | 500+ | **0.6569** |
| **CGGA-325** | RNA-Seq | 325 | **0.6325** |
| **CGGA-693** | RNA-Seq | 693 | **0.5793** |

---

## 🌐 Nguồn dữ liệu & Bản quyền

Dữ liệu được tổng hợp từ **TCGA (GDC)**, **CGGA**, và **NCBI GEO**. 
Mã nguồn phát hành dưới giấy phép **MIT**. Mọi đóng góp hoặc thắc mắc vui lòng liên hệ qua GitHub Issues.
