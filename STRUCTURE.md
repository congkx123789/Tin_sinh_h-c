# 📂 Cấu trúc Thư mục & Chi tiết Tệp tin (Project Structure)

Tài liệu này mô tả chi tiết sơ đồ tổ chức của dự án **GBM Survival Mamba** và chức năng của từng tệp tin mã nguồn.

---

## 🏗️ Sơ đồ Tổng quan
```text
gbm_survival_mamba/
├── checkpoints/          # Lưu trữ trọng số mô hình đã huấn luyện
├── data/                 # Cấu trúc thư mục dữ liệu (Trống trên GitHub)
├── models/               # Định nghĩa các kiến trúc mạng nơ-ron
├── results/              # Kết quả đầu ra (Biểu đồ, báo cáo)
├── scripts/              # Các kịch bản thực thi (Tiền xử lý, Training, Eval)
├── utils/                # Các hàm tiện ích bổ trợ
├── requirements.txt      # Danh sách thư viện cần thiết
└── README.md             # Tài liệu hướng dẫn chính
```

---

## 📝 Chi tiết chức năng từng thư mục

### 1. `models/` (Kiến trúc mô hình)
- **`autoencoder.py`**: Định nghĩa mạng **Denoising Autoencoder (DAE)** dùng để nén dữ liệu gen từ 16,383 chiều xuống 128 chiều.
- **`mamba_block.py`**: Lớp bao quanh (wrapper) thư viện **Mamba-SSM**, cho phép mô hình học các tương quan chuỗi.
- **`survival_net.py`**: Mô hình chính kết hợp Encoder và Mamba, bao gồm cả đầu ra dự đoán rủi ro (Survival) và đầu ra phân loại (Classification).
- **`__init__.py`**: Khởi tạo package models.

### 2. `scripts/` (Kịch bản thực thi - Quan trọng nhất)
- **`preprocess_data.py`**: Script tổng quát để làm sạch, lọc gen và chuẩn hóa dữ liệu RNA-seq.
- **`train_ae.py`**: Huấn luyện bộ Autoencoder để học không gian latent.
- **`train_mamba.py`**: Huấn luyện mô hình Mamba dự đoán sống sót (Survival training).
- **`evaluate.py`**: Đánh giá mô hình trên các bộ dữ liệu test, tính toán C-index và vẽ đường cong Kaplan-Meier.
- **`patient_gene_report.py`**: Trích xuất dữ liệu của một bệnh nhân cụ thể và tạo báo cáo rủi ro.
- **`extract_global_biomarkers.py`**: Sử dụng Gradient để tìm ra các gen có ảnh hưởng lớn nhất đến tiên lượng toàn cầu.
- **`visualize_classifier.py`**: Vẽ các biểu đồ ROC, Confusion Matrix và KM stratification.
- **`visualize_biomarker_landscape.py`**: Tạo Dashboard heatmap cho các dấu ấn sinh học.
- **`test_custom_patient.py`**: Cho phép người dùng đưa file gen của bệnh nhân mới vào để AI dự đoán rủi ro.
- **`analyze_treatment.py`**: Phân tích sự khác biệt về biểu hiện gen giữa các nhóm điều trị.
- **`sync_validation_data.py`**: Đồng bộ danh sách gen giữa các bộ dữ liệu khác nhau.

### 3. `utils/` (Hàm bổ trợ)
- **`loss.py`**: Triển khai hàm mất mát **Cox Partial Likelihood** tùy chỉnh cho bài toán sống sót.
- **`metrics.py`**: Chứa các hàm tính toán chỉ số **C-index** và các hàm thống kê sống sót.
- **`preprocessing.py`**: Các hàm phụ trợ cho việc lọc và chuẩn hóa dữ liệu.

### 4. `checkpoints/` (Trọng số mô hình)
- **`ae_weights/best_ae.pth`**: Trọng số tốt nhất của bộ Autoencoder.
- **`mamba_weights/best_mamba.pth`**: Trọng số mô hình Survival Mamba đã huấn luyện xong.
- **`mamba_weights/best_classifier.pth`**: Trọng số mô hình tối ưu cho bài toán phân loại.

### 5. `results/` (Kết quả)
- Thư mục này chứa toàn bộ các file `.png` (biểu đồ) và `.csv` (bảng kết quả biomarker) được sinh ra sau khi chạy các script trong thư mục `scripts/`.

---

## ⚙️ Các tệp tin gốc
- **`run.py`**: Điểm bắt đầu của dự án (Entry point), thường dùng để điều phối các tác vụ chính.
- **`requirements.txt`**: Danh sách tất cả các thư viện Python và phiên bản tương ứng để tái lập môi trường.
- **`.gitignore`**: Quy định các file/thư mục không được đẩy lên GitHub (như thư viện nặng, dữ liệu cá nhân, keys).
