# 🧬 GBM Survival Multi-modal: RNA-Seq & GATK Variants

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.0+-green.svg)](https://lightgbm.readthedocs.io/)
[![GATK](https://img.shields.io/badge/Bio-GATK-red.svg)](https://gatk.broadinstitute.org/)

Hệ thống tiên lượng đa phương thức kết hợp biểu hiện gen và biến thể di truyền cho bệnh nhân Glioblastoma (GBM).

---

## 🚀 Quy trình thực thi toàn diện (Full Pipeline)

Để sử dụng toàn bộ các phương pháp cải tiến, hãy thực hiện theo thứ tự sau:

### 1. Cài đặt môi trường
```bash
pip install -r requirements.txt
```

### 2. Tiền xử lý & Tích hợp GATK
```bash
python run.py preprocess
python run.py gatk
```

### 3. Huấn luyện mô hình đa phương thức
```bash
python run.py train_lightgbm
```

### 4. Giải thích mô hình & Trích xuất gen
```bash
python run.py explain
python run.py importance
```

### 5. Khởi chạy Dashboard tương tác
```bash
streamlit run dashboard.py
```

---

## 📊 Các phương pháp cốt lõi
- **Lasso Feature Selection**: Lọc nhiễu từ 16k gen xuống còn 23 gen chủ chốt.
- **GATK Variant Integration**: Bổ sung thông tin đột biến IDH/MGMT.
- **SHAP Interpretability**: Giải thích đóng góp của từng gen cho bệnh nhân.
- **Multi-modal LightGBM**: Mô hình dự đoán rủi ro dựa trên dữ liệu hỗn hợp.

---

## 📝 Tài liệu báo cáo
Toàn bộ nội dung đồ án chi tiết được lưu tại `REPORT.md` và `GRADUATION_THESIS.md`.
