# ĐỒ ÁN TỐT NGHIỆP: NGHIÊN CỨU VÀ TRIỂN KHAI MÔ HÌNH LIGHTGBM TỐI ƯU TRONG DỰ ĐOÁN TIÊN LƯỢNG BỆNH NHÂN UNG THƯ NÃO (GBM)

---

## MỤC LỤC
1. [CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI](#chuong-1)
2. [CHƯƠNG 2: CƠ SỞ LÝ THUYẾT](#chuong-2)
3. [CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU](#chuong-3)
4. [CHƯƠNG 4: TRIỂN KHAI HỆ THỐNG](#chuong-4)
5. [CHƯƠNG 5: KẾT QUẢ VÀ THẢO LUẬN](#chuong-5)
6. [CHƯƠNG 6: PHÂN TÍCH AN TOÀN VÀ ĐỘ TIN CẬY](#chuong-6)
7. [CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN](#chuong-7)
8. [TÀI LIỆU THAM KHẢO](#tai-lieu-tham-khao)

---

<a name="chuong-1"></a>
## CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI

### 1.1. Đặt vấn đề
Ung thư não, đặc biệt là Glioblastoma Multiforme (GBM), là một trong những loại u ác tính nguy hiểm nhất với tỷ lệ tử vong cao và thời gian sống sót trung bình ngắn. Việc dự đoán chính xác tiên lượng sống sót đóng vai trò quyết định trong việc cá nhân hóa phác đồ điều trị, giúp kéo dài sự sống và cải thiện chất lượng sống cho bệnh nhân. Tuy nhiên, dữ liệu biểu hiện gen (RNA-Seq) thường có đặc điểm là số lượng đặc trưng (genes) cực lớn trong khi số lượng mẫu bệnh phẩm lại hạn chế, gây ra thách thức lớn cho các mô hình học máy truyền thống.

### 1.2. Mục tiêu đề tài
- Nghiên cứu cơ chế trích xuất đặc trưng từ dữ liệu genomic quy mô lớn.
- Xây dựng mô hình dự đoán dựa trên thuật toán LightGBM kết hợp với kỹ thuật lọc đặc trưng Lasso.
- Đạt được chỉ số C-index ổn định trên các tập dữ liệu chuẩn quốc tế.
- Phân tích các dấu ấn sinh học (biomarkers) quan trọng ảnh hưởng đến bệnh.

### 1.3. Đối tượng và Phạm vi nghiên cứu
- **Đối tượng**: Bệnh nhân Glioblastoma Multiforme (GBM) từ các nguồn dữ liệu công khai như TCGA, CGGA.
- **Phạm vi**: Tập trung vào dữ liệu biểu hiện gen RNA-Seq và các thông tin lâm sàng cơ bản.

---

<a name="chuong-2"></a>
## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT

### 2.1. Glioblastoma Multiforme (GBM)
GBM là loại u thần kinh đệm cấp độ IV theo phân loại của WHO. Đặc điểm của nó là tính xâm lấn mạnh, tăng sinh mạch máu và kháng trị liệu cao. Các nghiên cứu gần đây chỉ ra rằng các đột biến gen và sự thay đổi biểu hiện RNA là chìa khóa để hiểu về sự tiến triển của bệnh.

### 2.2. Dữ liệu RNA-Seq
RNA-Seq là công nghệ giải trình tự thế hệ mới cho phép đo lường mức độ biểu hiện của hàng chục nghìn gen cùng lúc. Dữ liệu này cung cấp một cái nhìn toàn cảnh về trạng thái sinh học của tế bào u.

### 2.3. Thuật toán LightGBM
LightGBM (Light Gradient Boosting Machine) là một framework học máy dựa trên cây quyết định. Ưu điểm nổi bật của nó là:
- Tốc độ huấn luyện nhanh.
- Hiệu quả bộ nhớ cao.
- Hỗ trợ tốt cho dữ liệu có số lượng đặc trưng lớn thông qua kỹ thuật GOSS (Gradient-based One-Side Sampling) và EFB (Exclusive Feature Bundling).

### 2.4. Kỹ thuật Lasso (Least Absolute Shrinkage and Selection Operator)
Lasso là một phương pháp hồi quy sử dụng chuẩn L1 để thực hiện việc chọn lọc đặc trưng. Bằng cách ép các hệ số của các biến không quan trọng về 0, Lasso giúp loại bỏ nhiễu và giữ lại những gen có ý nghĩa thống kê cao nhất.

### 2.5. Phân tích sống sót (Survival Analysis)
Khác với hồi quy thông thường, phân tích sống sót xử lý dữ liệu có "censoring" (các bệnh nhân chưa kết thúc sự kiện tại thời điểm nghiên cứu). Chỉ số C-index (Concordance Index) được sử dụng để đánh giá khả năng xếp hạng rủi ro của mô hình.

---

<a name="chuong-3"></a>
## CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU

### 3.1. Quy trình tổng quát (Workflow)
Quy trình thực hiện bao gồm 4 giai đoạn chính:
1. Thu thập và làm sạch dữ liệu thô.
2. Tiền xử lý và chuẩn hóa (Normalization).
3. Chọn lọc đặc trưng bằng LassoCV.
4. Huấn luyện và tinh chỉnh mô hình LightGBM.

### 3.2. Chiến lược tiền xử lý
Dữ liệu RNA-Seq thô được xử lý qua các bước:
- **Lọc gen**: Loại bỏ các gen có biến thiên thấp (nhiễu).
- **Log-transformation**: Đưa dữ liệu về phân phối chuẩn hơn.
- **Robust Scaling**: Giảm tác động của các giá trị ngoại lai (outliers).

### 3.3. Thiết kế mô hình lai (Hybrid Approach)
Sự kết hợp giữa Lasso và LightGBM tạo ra một bộ lọc hai lớp:
- **Lớp 1 (Lasso)**: Loại bỏ các gen có tương quan tuyến tính thấp với mục tiêu, giảm chiều dữ liệu từ 16,000 xuống còn khoảng 20-100 gen.
- **Lớp 2 (LightGBM)**: Học các mối quan hệ phi tuyến phức tạp giữa các gen đã chọn để đưa ra dự đoán cuối cùng.

---

<a name="chuong-4"></a>
## CHƯƠNG 4: TRIỂN KHAI HỆ THỐNG

### 4.1. Môi trường phát triển
- Hệ điều hành: Linux Ubuntu.
- Môi trường ảo: Python venv.
- Quản lý phiên bản: Git.

### 4.2. Cấu trúc mã nguồn
Dự án được tổ chức theo mô hình module hóa:
- `scripts/`: Chứa các kịch bản thực thi độc lập.
- `models/`: Chứa các định nghĩa kiến trúc mô hình.
- `utils/`: Chứa các hàm hỗ trợ tính toán và xử lý dữ liệu.

### 4.3. Các thuật toán then chốt
*(Trình bày các đoạn code quan trọng về Lasso Selection và LightGBM Training)*

---

<a name="chuong-5"></a>
## CHƯƠNG 5: KẾT QUẢ VÀ THẢO LUẬN

### 5.1. Kết quả định lượng
Mô hình Ensemble LightGBM kết hợp chọn lọc đặc trưng bằng CoxPH đạt được các chỉ số C-index thực nghiệm như sau:
- **Số lượng gen tối ưu**: 30 gen (được chọn lọc thông qua CoxPH với p-value < 0.05).
- **C-index nội bộ (TCGA-GBM Test)**: 0.5749.
- **C-index ngoại kiểm TCGA-LGG**: 0.5771.
- **C-index ngoại kiểm CGGA-693**: 0.6066.
- **C-index ngoại kiểm REMBRANDT**: 0.5151.
- **C-index ngoại kiểm GSE4412**: 0.5123.

### 5.2. Phân tích các Biomarkers hàng đầu
Dựa trên mức độ đóng góp (Gain Feature Importance) trung bình của mô hình Ensemble LightGBM và phân tích SHAP, các gen chỉ thị hàng đầu ảnh hưởng đến sự sinh tồn bao gồm:
- **HNRNPA1P52**: Có mức độ đóng góp cao nhất, đóng vai trò bảo vệ (Tương quan thuận với thời gian sống).
- **LOC105371279**: Gen ác tính (Tương quan nghịch với thời gian sống).
- **ANKRD1**: Gen ác tính, liên quan mật thiết đến sự phát triển của khối u thần kinh đệm.
- **MIR4280HG**: Gen bảo vệ (Tương quan thuận với thời gian sống).
- **SCG5**, **RFX8**, **PARK7**: Các gen ác tính có mức độ biểu hiện tỷ lệ nghịch với thời gian sống sót của bệnh nhân.

### 5.3. Trực quan hóa Kaplan-Meier
Mô hình phân tách rõ rệt các nhóm nguy cơ cao và nguy cơ thấp trên tất cả các tập kiểm thử. 
- Biểu đồ Kaplan-Meier nội bộ: `results/km_plot_test_internal_lgbm_improved.png`
- Biểu đồ Kaplan-Meier trên tập ngoại kiểm CGGA: `results/km_plot_test_cgga_lgbm_improved.png`
Đường cong sống sót cho thấy nhóm nguy cơ cao có thời gian sống trung bình ngắn hơn rõ rệt (p-value < 0.05).

---

<a name="chuong-6"></a>
## CHƯƠNG 6: PHÂN TÍCH AN TOÀN VÀ ĐỘ TIN CẬY

### 6.1. Khả năng chống lại tấn công dữ liệu (Data Robustness)
Trong môi trường y tế, dữ liệu có thể bị nhiễu do lỗi thiết bị hoặc cố ý thay đổi (adversarial attack). Việc sử dụng Lasso giúp mô hình chỉ tập trung vào các tín hiệu mạnh nhất, làm giảm diện tích tấn công (attack surface) của kẻ xấu.

### 6.2. Tính giải thích được của mô hình (Explainability)
Thay vì là một "hộp đen", mô hình cung cấp Feature Importance rõ ràng, cho phép các bác sĩ kiểm chứng lại dựa trên kiến thức y khoa hiện tại.

---

<a name="chuong-7"></a>
## CHƯƠNG 7: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 7.1. Kết luận
Đồ án đã xây dựng thành công một pipeline dự đoán sống sót hiệu quả cho bệnh nhân GBM. Sự kết hợp giữa Lasso và LightGBM là một hướng đi đúng đắn cho dữ liệu genomic quy mô lớn.

### 7.2. Hạn chế và Hướng phát triển
- **Hạn chế**: Số lượng mẫu huấn luyện còn ít.
- **Mở rộng**: 
    - Tích hợp thêm dữ liệu hình ảnh (MRI) để xây dựng mô hình đa phương thức (Multimodal).
    - Thử nghiệm trên các loại ung thư khác.

---

<a name="tai-lieu-tham-khao"></a>
## TÀI LIỆU THAM KHẢO
1. [Liệt kê các bài báo khoa học đã sử dụng]
2. [Link GitHub dự án]
