# 🗺️ Bản đồ Chi tiết Dự án (Deep-Dive Project Structure)

Chào mừng bạn đến với hướng dẫn chi tiết về cấu trúc của dự án **GBM Survival Mamba**. Tài liệu này không chỉ liệt kê tệp tin mà còn giải thích **Logic** và **Thứ tự thực hiện** của toàn bộ hệ thống.

---

## 🧭 1. Sơ đồ Cấu trúc Tổng thể
```text
gbm_survival_mamba/
├── 📂 models/           # "BỘ NÃO": Nơi định nghĩa các thuật toán AI
├── 📂 scripts/          # "CÁNH TAY": Các lệnh thực thi từng bước
├── 📂 utils/            # "CÔNG CỤ": Các hàm tính toán bổ trợ
├── 📂 checkpoints/      # "KÝ ỨC": Lưu trữ các kết quả đã huấn luyện
├── 📂 results/          # "THÀNH QUẢ": Biểu đồ và báo cáo trích xuất
└── 📄 run.py            # "ĐIỀU PHỐI": File chạy chính của dự án
```

---

## 🛠️ 2. Chi tiết theo Giai đoạn Thực hiện (Workflow)

Tôi chia dự án thành 4 giai đoạn chính để bạn dễ theo dõi:

### Giai đoạn A: Tiền xử lý Dữ liệu (Data Preparation)
*Nhiệm vụ: Biến dữ liệu gen thô thành dạng mà AI có thể hiểu được.*

| Tệp tin | Chức năng chi tiết | Khi nào dùng? |
| :--- | :--- | :--- |
| **`scripts/preprocess_data.py`** | Lọc bỏ các gen không quan trọng, thực hiện Log-transform để chuẩn hóa dữ liệu. | **Bước 1**: Chạy đầu tiên khi có dữ liệu mới. |
| **`scripts/sync_validation_data.py`** | Đảm bảo các bộ dữ liệu khác (CGGA, GEO) có cùng danh sách gen với bộ huấn luyện (TCGA). | Chạy sau khi đã có dữ liệu huấn luyện chuẩn. |
| **`utils/preprocessing.py`** | Chứa các công thức toán học để làm sạch dữ liệu. | Được gọi tự động bởi các script trên. |

### Giai đoạn B: Huấn luyện AI (Model Training)
*Nhiệm vụ: Dạy cho AI cách nén gen và dự đoán rủi ro sống sót.*

| Tệp tin | Chức năng chi tiết | Logic bên trong |
| :--- | :--- | :--- |
| **`models/autoencoder.py`** | Định nghĩa kiến trúc nén gen. | Nén 16k gen xuống 128 đặc trưng cốt lõi. |
| **`scripts/train_ae.py`** | Thực hiện việc dạy bộ nén gen. | Lưu kết quả vào `checkpoints/ae_weights/`. |
| **`models/mamba_block.py`** | Định nghĩa lớp Mamba (State Space Model). | Học mối quan hệ chuỗi giữa các nhóm gen. |
| **`models/survival_net.py`** | Kết hợp nén gen và Mamba để dự đoán. | Là file chứa "linh hồn" của kiến trúc Hybrid. |
| **`scripts/train_mamba.py`** | Thực hiện dạy AI dự đoán sống sót. | Sử dụng hàm mất mát Cox trong `utils/loss.py`. |

### Giai đoạn C: Đánh giá & Kiểm chứng (Evaluation)
*Nhiệm vụ: Kiểm tra xem AI dự đoán chính xác đến đâu.*

| Tệp tin | Chức năng chi tiết | Kết quả trả về |
| :--- | :--- | :--- |
| **`scripts/evaluate.py`** | Tính toán chỉ số C-index trên các bộ dữ liệu. | Trả về con số độ chính xác (ví dụ: 0.65). |
| **`utils/metrics.py`** | Công thức tính C-index và Kaplan-Meier. | Được gọi bởi script đánh giá. |
| **`scripts/visualize_classifier.py`** | Vẽ biểu đồ ROC, ma trận nhầm lẫn. | Lưu ảnh vào `results/classification/`. |

### Giai đoạn D: Ứng dụng & Báo cáo (Application)
*Nhiệm vụ: Sử dụng AI để giúp bác sĩ/nhà khoa học đưa ra quyết định.*

| Tệp tin | Chức năng chi tiết | Ứng dụng thực tế |
| :--- | :--- | :--- |
| **`scripts/test_custom_patient.py`** | Nhập 1 mẫu bệnh nhân mới và xem AI dự đoán. | Dùng cho bác sĩ khi có bệnh nhân mới. |
| **`scripts/patient_gene_report.py`** | Xuất file ảnh báo cáo chi tiết cho bệnh nhân. | Dùng để in ra kẹp vào hồ sơ bệnh án. |
| **`scripts/extract_global_biomarkers.py`** | Tìm ra 20 gen "nguy hiểm" nhất. | Giúp nhà khoa học tìm mục tiêu thuốc mới. |
| **`scripts/visualize_biomarker_landscape.py`**| Vẽ bản đồ gen tổng thể của dự án. | Dùng cho báo cáo khoa học hoặc thuyết trình. |

---

## 💾 3. Các file hệ thống khác
- **`requirements.txt`**: "Danh sách mua sắm" - chứa các thư viện bạn cần cài để máy chạy được code.
- **`.gitignore`**: "Tấm khiên" - ngăn không cho các file rác hoặc dữ liệu riêng tư bị đẩy lên mạng.
- **`checkpoints/*.pth`**: "Bộ nhớ" - Đây là các file nặng nhất, chứa toàn bộ kiến thức AI đã học được. Không có nó, code chỉ là cái vỏ không hồn.

---
**Ghi chú**: Mọi biểu đồ bạn thấy trong dự án đều nằm trong thư mục `results/`. Nếu bạn chạy lại code, các file trong này sẽ được cập nhật mới.
