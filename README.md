# 🧬 GBM Survival Prediction using Mamba-SSM

Mô hình học sâu tiên tiến sử dụng kiến trúc **Mamba (Selective State Space Model)** để dự đoán tiên lượng sống sót của bệnh nhân Ung thư não (Glioblastoma Multiforme - GBM) dựa trên dữ liệu biểu hiện gen (RNA-Seq).

---

## 🕒 Nhật ký Quy trình thực hiện (Step-by-Step)

Dưới đây là chi tiết từng bước mà dự án đã thực hiện để xây dựng hệ thống dự đoán sinh tồn:

### Bước 1: Thu thập và Quản lý Dữ liệu thô (Data Acquisition)
- **Nguồn dữ liệu**: Tải dữ liệu RNA-Seq (FPKM), thông tin lâm sàng và dữ liệu sinh tồn của dự án **TCGA-GBM** từ S3 Xena Hub.
- **Xử lý sự cố lỗi Map Gen**: Phát hiện file Gencode mapping nguyên bản bị hỏng. Đã triển khai giải pháp thay thế bằng cách truy vấn trực tiếp **MyGene.info API** để giải mã hơn 60,000 mã Ensembl ID sang Gene Symbols chuẩn quốc tế.

### Bước 2: Tiền xử lý & Kỹ thuật Sinh tin học (Preprocessing)
- **Lọc dữ liệu**: Đồng bộ hóa dữ liệu RNA-Seq và dữ liệu Survival (loại bỏ các mẫu thiếu thông tin sinh tồn).
- **Phép toán Log2**: Chuyển đổi dữ liệu biểu hiện gen sang thang đo Log2 (`log2(FPKM + 1)`) để giảm độ lệch (skewness).
- **Chuẩn hóa Z-score**: Sử dụng `StandardScaler` để đưa biểu hiện của gen về cùng một phân phối (Mean=0, Std=1).
- **Lọc Gen (Feature Selection)**: Giữ lại **16,504 gen** có độ biến thiên cao nhất để đảm bảo mô hình tập trung vào các tín hiệu sinh học quan trọng.

### Bước 3: Nén đặc trưng với Denoising Autoencoder (DAE)
- Xây dựng mạng Encoder-Decoder để học cách biểu diễn dữ liệu gen ở không gian tiềm ẩn (Latent space) **128 chiều**.
- Cơ chế Denoising giúp mô hình bền vững hơn trước các nhiễu sinh học và batch-effect.

### Bước 4: Thiết kế Kiến trúc Mamba-SSM (Advanced Modeling)
- **Băm chuỗi (Reshaping)**: Thực hiện kỹ thuật băm vector tiềm ẩn 128-dim thành chuỗi **8 token** (mỗi token 16-dim). 
- **Lý do**: Giúp khối Mamba có thể quét qua chuỗi như dữ liệu ngôn ngữ/thời gian, tìm ra mối tương tác chéo giữa các nhóm gen.
- **Hệ thống hóa**: Sử dụng hàng đợi các Mamba Block để tính toán Risk Score (Log Hazard Ratio).

### Bước 5: Huấn luyện & Phân tầng Sinh tồn
- **Hàm mất mát**: Sử dụng **Cox Partial Likelihood Loss** (Negative Log Likelihood).
- **Phân chia dữ liệu**: Sử dụng phương pháp **Stratified Split (70/15/15)** để đảm bảo tỷ lệ bệnh nhân tử vong đồng đều giữa tập Training và Testing.
- **Tổ chức**: Tự động chia file vào các thư mục `train/`, `val/`, `test_internal/`.

### Bước 6: Kiểm chứng ngoại kiểm (External Validation)
- Triển khai kiểm tra độ tin cậy của mô hình trên bộ dữ liệu **TCGA-LGG** (Lower Grade Glioma).
- Mục tiêu: Chứng minh mô hình có thể tổng quát hóa kiến thức từ ung thư não cấp độ cao sang các cấp độ thấp hơn.

---

## 🏗 Cấu trúc mã nguồn (Code Structure)

```text
gbm_survival_mamba/
├── data/
│   ├── raw/               # Chứa dữ liệu gốc (.tsv.gz)
│   └── processed/         # Dữ liệu sạch đã chia folder
│       ├── train/         # Dữ liệu huấn luyện
│       ├── val/           # Dữ liệu kiểm chứng (validation)
│       ├── test_internal/ # Dữ liệu test nội bộ (GBM)
│       └── test_lgg/      # Dữ liệu test ngoại kiểm (LGG)
├── models/                # Autoencoder, Mamba, Survival Head
├── scripts/               # Các script chạy pipeline (Preprocess, Train, Evaluate)
├── utils/                 # Metrics (C-index, KM Curve), API Mapping, Logic xử lý
└── results/               # Biểu đồ Kaplan-Meier và kết quả đánh giá
```

## 📊 Kết quả đạt được

*   **Chỉ số Concordance (C-index)**: **0.6151** (Vượt mức 0.6 - mục tiêu ban đầu của dự án).
*   **Kaplan-Meier Plot**: Thấy rõ sự phân tách sinh tồn giữa nhóm High-Risk và Low-Risk.

---
**Dự án đang trong giai đoạn kiểm chứng trên tập dữ liệu ngoại kiểm LGG.**
