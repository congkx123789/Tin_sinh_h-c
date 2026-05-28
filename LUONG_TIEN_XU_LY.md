# LUỒNG TIỀN XỬ LÝ DỮ LIỆU RNA-SEQ NÂNG CAO (RNA-SEQ CLEANING PIPELINE)

Hệ thống tiên lượng đa phương thức triển khai một đường ống tiền xử lý dữ liệu biểu hiện gen thô cực kỳ nghiêm ngặt nhằm giảm số chiều dữ liệu, loại bỏ nhiễu sinh học và kỹ thuật, điền khuyết các giá trị thiếu, và chuẩn hóa thang đo của dữ liệu. 

Dưới đây là sơ đồ kiến trúc logic và diễn giải chi tiết từng bước triển khai trong class `RNASeqCleaner` (định nghĩa tại file [preprocessing.py](file:///d:/Tin_sinh_h-c/utils/preprocessing.py)).

---

## Sơ đồ logic luồng xử lý (Data Flowchart)

![Sơ đồ logic tiền xử lý](results/preprocessing_logic.png)

---

## Chi tiết các bước triển khai logic

### Bước 1: Lọc gen có mức độ biểu hiện và độ biến thiên thấp (Low-Expression & Variance Filtering)
*   **Mục đích:** Giảm thiểu số chiều của ma trận gen biểu hiện thô (ban đầu hơn 16.000 gen) trước khi đưa vào các bước tính toán đắt đỏ phía sau.
*   **Logic thực hiện:**
    *   **Lọc biểu hiện thấp:** Loại bỏ các gen không được biểu hiện ở phần lớn các mẫu bệnh nhân. Một gen được giữ lại nếu tỷ lệ số mẫu có giá trị biểu hiện lớn hơn 0 đạt ít nhất 20% (ngưỡng `expression_ratio = 0.2`).
    *   **Lọc biến thiên thấp:** Loại bỏ các gen có mức độ biểu hiện gần như không đổi trên tất cả các bệnh nhân, vì chúng không mang thông tin phân tầng sinh tồn. Hệ thống chỉ giữ lại các gen có phương sai lớn hơn ngưỡng `variance_threshold = 0.1` (trong code thực thi).

### Bước 2: Điền khuyết dữ liệu bằng thuật toán KNN (KNN Imputer)
*   **Mục đích:** Khắc phục tình trạng khuyết thiếu dữ liệu (missing values) phát sinh từ giới hạn của công nghệ giải trình tự gen.
*   **Logic thực hiện:**
    *   Sử dụng thuật toán **K-Nearest Neighbors Imputer (KNN Imputer)** với tham số $K = 5$.
    *   Hệ thống tìm kiếm 5 mẫu bệnh nhân có cấu hình biểu hiện gen tương đồng nhất với mẫu bị khuyết dựa trên khoảng cách hình học (Euclid) trên không gian đa chiều.
    *   Giá trị bị khuyết được tính bằng trung bình có trọng số từ 5 mẫu láng giềng này. Phương pháp này giúp giữ nguyên mối tương quan sinh học đa biến tự nhiên giữa các cụm gen tương tác thay vì điền giá trị trung bình thô sơ làm bẹt phân phối dữ liệu.

### Bước 3: Phát hiện và loại bỏ mẫu bệnh nhân dị biệt (Isolation Forest)
*   **Mục đích:** Loại bỏ các mẫu bệnh nhân có chất lượng giải trình tự kém, mẫu bị nhiễm bẩn sinh học hoặc sai lệch hồ sơ bệnh án để tránh gây nhiễu cho mô hình học máy.
*   **Logic thực hiện:**
    *   Áp dụng thuật toán **Isolation Forest** (Rừng cô lập) trên ma trận biểu hiện gen đã điền khuyết với tham số tỷ lệ dị biệt thiết lập trước `contamination = 0.05` (loại bỏ 5% số lượng mẫu dị biệt nhất).
    *   Thuật toán hoạt động bằng cách xây dựng ngẫu nhiên các cây phân tách. Các điểm dị biệt nằm xa phân phối chung sẽ dễ dàng bị cô lập hơn và có độ dài đường đi từ gốc đến lá cực kỳ ngắn. Những bệnh nhân được phân loại là mẫu dị biệt sẽ bị loại bỏ hoàn toàn khỏi tập huấn luyện.

### Bước 4: Biến đổi Log1p đưa về phân phối chuẩn (Log1p Transformation)
*   **Mục đích:** Xử lý hiện tượng phân phối lệch phải cực kỳ nặng (một vài gen biểu hiện cực mạnh có giá trị rất lớn) đặc trưng của dữ liệu sinh học.
*   **Logic thực hiện:**
    *   Áp dụng phép biến đổi phi tuyến logarit tự nhiên cộng thêm một đơn vị (`np.log1p`).
    *   Phép toán này làm co hẹp dải giá trị cực đại, giúp đưa phân phối dữ liệu biểu hiện gen về dạng đối xứng hơn (gần phân phối chuẩn), làm giảm thiểu sai số thay đổi lớn và hỗ trợ các thuật toán tối ưu học máy hội tụ nhanh hơn.

### Bước 5: Chuẩn hóa chống mẫu dị biệt đặc trưng (Robust Scaler)
*   **Mục đích:** Đưa các gen về cùng một thang đo đồng nhất mà không làm triệt tiêu các đặc trưng đột biến mang giá trị chẩn đoán lâm sàng quan trọng.
*   **Logic thực hiện:**
    *   Sử dụng phương pháp **Robust Scaler** thay thế cho StandardScaler truyền thống (vốn nhạy cảm với outliers).
    *   Robust Scaler thực hiện căn chỉnh dải dữ liệu dựa trên **Trung vị (Median)** và **Khoảng biến thiên tứ phân vị (IQR)** của từng đặc trưng gen. Phép toán này giúp bảo toàn được các giá trị đột biến biểu hiện cực đoan của tế bào ung thư (vốn mang thông tin sinh tồn cốt lõi) đồng thời đảm bảo thang đo của các đặc trưng đồng đều nhau.
