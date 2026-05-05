# 🗺️ Bản đồ Toàn diện Dự án (Full Project Tree Map)

Tài liệu này trình bày toàn bộ cấu trúc tệp tin của dự án **GBM Survival Mamba** dưới dạng sơ đồ cây trực quan kèm ghi chú chức năng.

---

## 🧭 1. Sơ đồ Cấu trúc Chi tiết (Full Tree)

```text
gbm_survival_mamba/
├── 📂 models/                  # "BỘ NÃO": Định nghĩa kiến trúc AI
│   ├── 📄 __init__.py          # Khởi tạo package models
│   ├── 📄 autoencoder.py       # Kiến trúc nén gen Denoising Autoencoder (DAE)
│   ├── 📄 mamba_block.py       # Wrapper cho lớp Mamba-SSM (Học chuỗi)
│   └── 📄 survival_net.py      # Mô hình tổng hợp Survival & Classification
│
├── 📂 scripts/                 # "CÁNH TAY": Các kịch bản thực thi trực tiếp
│   ├── 📂 __pycache__/         # (Tệp tin đệm, tự động sinh ra)
│   ├── 📄 analyze_treatment.py  # Phân tích ảnh hưởng của thuốc/điều trị
│   ├── 📄 evaluate.py          # Đánh giá C-index và vẽ biểu đồ KM
│   ├── 📄 evaluate_classifier_metrics.py # Tính toán AUC/ROC cho phân loại
│   ├── 📄 extract_biomarkers.py # Trích xuất các gen quan trọng cấp độ mẫu
│   ├── 📄 extract_global_biomarkers.py # Tìm 20 gen "tử thần" toàn dự án
│   ├── 📄 fast_download.py      # Script tải nhanh dữ liệu (nếu cần)
│   ├── 📄 patient_gene_report.py # Xuất báo cáo rủi ro cho 1 bệnh nhân
│   ├── 📄 predict_condition.py  # Dự đoán trạng thái bệnh từ gen
│   ├── 📄 preprocess_data.py    # Script TIỀN XỬ LÝ chính (Lọc gen/Log-transform)
│   ├── 📄 sync_validation_data.py # Đồng bộ gen giữa các tập dữ liệu khác nhau
│   ├── 📄 test_custom_patient.py # Nhập bệnh nhân mới để AI dự đoán
│   ├── 📄 train_ae.py           # Huấn luyện bộ nén gen (DAE Training)
│   ├── 📄 train_classifier.py   # Huấn luyện mô hình phân loại rủi ro
│   ├── 📄 train_mamba.py        # Huấn luyện mô hình SỐNG SÓT chính
│   ├── 📄 visualize_biomarker_landscape.py # Vẽ Dashboard bản đồ gen
│   └── 📄 visualize_classifier.py # Vẽ ROC, Confusion Matrix, KM stratification
│
├── 📂 utils/                   # "CÔNG CỤ": Các hàm toán học bổ trợ
│   ├── 📄 loss.py              # Định nghĩa hàm mất mát Cox Partial Likelihood
│   ├── 📄 metrics.py           # Công thức tính C-index & Log-rank test
│   └── 📄 preprocessing.py     # Các hàm nhỏ phục vụ làm sạch dữ liệu
│
├── 📂 checkpoints/             # "KÝ ỨC": Nơi lưu trữ bộ não AI đã học
│   ├── 📂 ae_weights/          # Trọng số của bộ nén Autoencoder
│   └── 📂 mamba_weights/       # Trọng số của mô hình Mamba & Classifier
│
├── 📂 results/                 # "THÀNH QUẢ": Biểu đồ & báo cáo đã xuất
│   ├── 📂 biomarkers/          # Các ảnh và CSV về dấu ấn sinh học
│   ├── 📂 classification/      # Các ảnh ROC, Confusion Matrix
│   └── 📄 *.png                # Các biểu đồ Kaplan-Meier tổng hợp
│
├── 📂 data/                    # "NGUYÊN LIỆU": (Trống trên GitHub - xem DATA_MAP.md)
│
├── 📄 .gitignore               # "TẤM KHIÊN": Chặn các file rác đẩy lên GitHub
├── 📄 README.md                # "HƯỚNG DẪN": Tài liệu chính của dự án
├── 📄 STRUCTURE.md             # "BẢN ĐỒ": (Chính là file bạn đang đọc)
├── 📄 requirements.txt         # "THƯ VIỆN": Danh sách các gói cần cài đặt
└── 📄 run.py                   # "ĐIỀU PHỐI": File khởi động/chạy tổng hợp
```

---

## 💡 2. Ý nghĩa các biểu tượng
- 📂 **Thư mục**: Chứa các nhóm tệp tin có cùng mục đích.
- 📄 **Tệp tin (.py)**: Mã nguồn Python chứa logic xử lý.
- 📄 **Tệp tin (.pth)**: "Bộ não" - trọng số nơ-ron đã được huấn luyện.
- 📄 **Tệp tin (.png)**: "Kết quả" - các biểu đồ trực quan hóa dữ liệu.

---

## 🚀 3. Thứ tự Chạy (Quick Flow)
Nếu bạn bắt đầu từ đầu, hãy đi theo sơ đồ này:
1. `scripts/preprocess_data.py` (Làm sạch dữ liệu)
2. `scripts/train_ae.py` (Dạy bộ nén gen)
3. `scripts/train_mamba.py` (Dạy bộ dự đoán sống sót)
4. `scripts/evaluate.py` (Kiểm tra kết quả)
5. `scripts/patient_gene_report.py` (Xuất báo cáo cuối cùng)
