# KỊCH BẢN THUYẾT TRÌNH CHI TIẾT (THỜI LƯỢNG 10 - 15 PHÚT)
**DỰ ÁN TIN SINH HỌC: NGHIÊN CỨU VỀ GLIOBLASTOMA PROGNOSTIC SOLUTIONS**
*Nhóm thực hiện: Hà Vũ Công & Trần Thị Hà Giang (Nhóm 6)*
*Giảng viên hướng dẫn: GS. TS. Lê Sỹ Vinh - Trường Đại học Công nghệ - ĐHQGHN*

---

## LỜI KHUYÊN TRƯỚC KHI TRÌNH BÀY
*   **Tốc độ nói:** Duy trì tốc độ vừa phải (khoảng 110 - 120 từ/phút), nhấn giọng ở các thuật ngữ kỹ thuật quan trọng.
*   **Cương nhu đúng lúc:** Khi chiếu các slide có hình vẽ kiến trúc (Slide 4, 6, 10, 11, 12, 14), hãy dùng con trỏ laser chỉ trực tiếp vào các khối mô hình để tăng tính thuyết phục.
*   **Chuyển slide mượt mà:** Sử dụng các câu nối đã được thiết kế sẵn ở cuối kịch bản của mỗi slide.

---

### SLIDE 1: GIỚI THIỆU ĐỀ TÀI (Thời lượng gợi ý: 45 giây)
*   **Nội dung hiển thị:** Logo UET, tên Khoa CNTT, tên Đề tài: "NGHIÊN CỨU VỀ GLIOBLASTOMA PROGNOSTIC SOLUTIONS - HỆ THỐNG TIÊN LƯỢNG SINH TỒN ĐA PHƯƠNG THỨC CHO BỆNH NHÂN U NÃO ĐỆM", tên GVHD và 2 thành viên nhóm thực hiện.
*   **Kịch bản nói chi tiết:**
    > "Kính thưa thầy giáo hướng dẫn GS. TS. Lê Sỹ Vinh cùng toàn thể các bạn sinh viên đang có mặt trong buổi báo cáo dự án Tin sinh học ngày hôm nay. Chúng em là nhóm 6, gồm hai thành viên: em là Hà Vũ Công và bạn Trần Thị Hà Giang.
    >
    > Hôm nay, đại diện cho nhóm nghiên cứu, em xin phép được trình bày báo cáo dự án với đề tài: **'Nghiên cứu về Glioblastoma Prognostic Solutions (GPS) - Xây dựng hệ thống tiên lượng sinh tồn đa phương thức sử dụng học máy và học sâu tích hợp'**.
    >
    > Đây là một nghiên cứu giao thoa giữa y sinh học hiện đại và khoa học máy tính tiên tiến, hướng tới mục tiêu tối ưu hóa phác đồ điều trị cá nhân hóa cho bệnh nhân ung thư não ác tính. Sau đây, em xin phép bắt đầu phần trình bày của nhóm."
*   **Lời nối chuyển slide:** *"Trước hết, chúng ta cần tìm hiểu xem động lực lâm sàng và bài toán y học thực tế nào đã thúc đẩy nhóm chúng em thực hiện đề tài này. Xin mời thầy và các bạn cùng hướng mắt lên Slide 2."*

---

### SLIDE 2: ĐẶT VẤN ĐỀ VÀ MỤC TIÊU LÂM SÀNG (Thời lượng gợi ý: 1 phút)
*   **Nội dung hiển thị:** Các điểm chính về Clinical Problem (Độ ác tính u não GBM, thời gian sống trung bình cực ngắn 12-15 tháng) và Research Objective (Cá nhân hóa tiên lượng sống sót, phân tầng rủi ro hóa/xạ trị TMZ).
*   **Kịch bản nói chi tiết:**
    > "Ung thư não đệm ác tính Glioblastoma Multiforme, hay viết tắt là GBM, được y văn thế giới ghi nhận là một trong những khối u nguyên phát ở não ác tính nhất và khó điều trị nhất ở người trưởng thành. Dù y học hiện đại đã áp dụng phác đồ chuẩn Stupp bao gồm phẫu thuật triệt căn tối đa kết hợp xạ trị và hóa trị bằng hóa chất Temozolomide (TMZ), thời gian sống thêm trung bình của bệnh nhân kể từ khi phát hiện bệnh vẫn cực kỳ ngắn ngủi, chỉ vỏn vẹn từ 12 đến 15 tháng, với tỷ lệ sống sót sau 5 năm nhỏ hơn 5%.
    >
    > Nguyên nhân sâu xa nằm ở **tính bất đồng nhất cực kỳ lớn** giữa các bệnh nhân. Hai khối u có biểu hiện hình ảnh học MRI giống nhau hoàn toàn có thể sở hữu hồ sơ đột biến DNA và biểu hiện gen phiên mã RNA khác biệt một trời một vực, dẫn tới phản ứng hóa trị khác nhau.
    >
    > Chính vì vậy, mục tiêu của dự án là xây dựng hệ thống **Survival Prediction (Tiên lượng sinh tồn)** cá nhân hóa, tự động phân tầng nguy cơ rủi ro thành nhóm High-risk và Low-risk. Công cụ này sẽ là cánh tay nối dài giúp các bác sĩ lâm sàng đưa ra quyết định phác đồ điều trị tích cực hoặc bảo tồn một cách chính xác nhất."
*   **Lời nối chuyển slide:** *"Tuy nhiên, để xử lý được nguồn dữ liệu y sinh đa chiều này, nhóm nghiên cứu đã phải đối mặt với ba thách thức kỹ thuật rất lớn mà chúng em sẽ phân tích ngay sau đây."*

---

### SLIDE 3: THÁCH THỨC DỮ LIỆU Y SINH (DATA CHALLENGES) (Thời lượng gợi ý: 1 phút)
*   **Nội dung hiển thị:** 3 bài toán khó: Curse of Dimensionality ($p \gg n$), Domain Shift (TCGA vs CGGA, RNA-Seq vs Microarray), Right-Censored Data (hiện tượng khuyết góc phải).
*   **Kịch bản nói chi tiết:**
    > "Thách thức đầu tiên là **Curse of Dimensionality - Lời nguyền đa chiều**. Số lượng đặc trưng gen biểu hiện phiên mã thường vượt quá 16.000 chiều, trong khi số lượng mẫu bệnh nhân thu thập được lại rất hạn chế, thường dưới 500 mẫu. Tỷ lệ này cực kỳ dễ khiến các mô hình học máy truyền thống rơi vào trạng thái 'quá khớp' - tức là chỉ học vẹt trên tập huấn luyện mà không dự đoán được mẫu mới.
    >
    > Thách thức thứ hai là **Domain Shift - Dịch chuyển phân phối**. Các nguồn dữ liệu sinh học phân tử bị ảnh hưởng sâu sắc bởi chủng tộc và nền tảng đo đạc công nghệ. Dữ liệu TCGA chủ yếu từ bệnh nhân Âu-Mỹ, sử dụng giải trình tự RNA-Seq; trong khi dữ liệu CGGA thu thập từ bệnh nhân Châu Á, và tập REMBRANDT lại đo bằng công nghệ lai Microarray thế hệ cũ. Sự khác biệt về nhiễu hệ thống này khiến việc chuyển giao mô hình trở nên vô cùng khó khăn.
    >
    > Cuối cùng và quan trọng nhất là **Right-Censored Data - Dữ liệu khuyết góc phải**. Trong nghiên cứu y khoa, tại thời điểm kết thúc theo dõi, nhiều bệnh nhân vẫn còn sống hoặc tự ý bỏ cuộc. Chúng ta không biết thời điểm tử vong thực tế của họ mà chỉ biết họ đã sống sót ít nhất đến ngày thứ $T$. Hiện tượng này khiến các hàm Loss hồi quy thông thường như MSE hay MAE hoàn toàn mất hiệu lực."
*   **Lời nối chuyển slide:** *"Để giải quyết triệt để đồng thời cả ba bài toán hóc búa này, nhóm 6 đã thiết kế một luồng xử lý và kiến trúc hệ thống tích hợp đa tầng. Xin mời thầy và các bạn theo dõi sơ đồ tổng quan trên Slide 4."*

---

### SLIDE 4: KIẾN TRÚC HỆ THỐNG TỔNG QUAN (Thời lượng gợi ý: 1 phút 15 giây)
*   **Nội dung hiển thị:** Hình vẽ `system_pipeline.png` thể hiện các khối từ dữ liệu đầu vào, tiền xử lý, chọn lọc đặc trưng đến 2 mô hình huấn luyện song song (LightGBM & SurvivalMambaNet) và kết quả giải thích SHAP.
*   **Kịch bản nói chi tiết:**
    > "Trên màn hình là kiến trúc tổng quan hệ thống **Glioblastoma Prognostic Solutions (GPS)** do chúng em thiết kế. Hệ thống nhận đầu vào đa phương thức bao gồm ma trận biểu hiện gen phiên mã RNA-Seq kết hợp nhãn đột biến DNA di truyền trích xuất từ GATK.
    >
    > Luồng xử lý gồm 5 khối chức năng chính:
    >
    > *Khối 1:* Tiền xử lý dữ liệu để làm sạch nhiễu đo đạc và nội suy các điểm khuyết thiếu.
    >
    > *Khối 2:* Lọc đặc trưng đa tầng sử dụng Spearman và mô hình CoxPH phạt L2 để chọn lọc ra các dấu ấn sinh học cốt lõi nhất.
    >
    > *Khối 3 và Khối 4:* Chúng em phát triển song song hai kiến trúc bổ trợ nhau. Một bên là **Ensemble LightGBM** - thuật toán học máy hiệu năng cao giúp bắt các tương tác phi tuyến nông. Bên còn lại là **DAE-SurvivalMambaNet** - mô hình học sâu kết hợp giữa mạng tự mã hóa khử nhiễu DAE và kiến trúc không gian trạng thái chọn lọc Mamba để trích xuất cấu trúc ẩn sâu kháng nhiễu.
    >
    > Cuối cùng, kết quả dự báo điểm nguy cơ lâm sàng sẽ được đưa qua mô hình giải thích **SHAP** để trực quan hóa, tạo điều kiện cho y bác sĩ hiểu rõ nguyên nhân sinh học đằng sau dự đoán."
*   **Lời nối chuyển slide:** *"Đi vào chi tiết cấu tạo hệ thống, chúng ta sẽ xem xét quy trình tiền xử lý dữ liệu biểu hiện gen thô thông qua lớp xử lý đặc thù RNASeqCleaner."*

---

### SLIDE 5: TIỀN XỬ LÝ DỮ LIỆU - PHẦN 1: LÀM SẠCH VÀ NỘI SUY (Thời lượng gợi ý: 45 giây)
*   **Nội dung hiển thị:** Các tham số kỹ thuật của Gene Expression Filtering (expression ratio = 0.2, variance threshold = 0.1) và KNN Imputation (K = 5).
*   **Kịch bản nói chi tiết:**
    > "Dữ liệu biểu hiện gen RNA-Seq thô chứa một lượng lớn gen rác không hoạt động hoặc phương sai bằng không. Chúng em thiết lập hai bộ lọc:
    >
    > Đầu tiên là lọc gen biểu hiện thấp, loại bỏ các gen có giá trị bằng không ở hơn 80% mẫu (`expression_ratio = 0.2`). 
    >
    > Tiếp theo là lọc phương sai thấp, loại bỏ các gen tĩnh có phương sai dưới `0.1` do chúng không mang thông tin phân hóa.
    >
    > Để xử lý vấn đề khuyết thiếu dữ liệu (missing values) phát sinh trong quá trình lưu trữ bệnh án, chúng em áp dụng thuật toán **KNN Imputer với K = 5**. Thay vì xóa bỏ mẫu bệnh nhân quý giá, thuật toán sẽ đo khoảng cách Euclid đa chiều để tìm ra 5 bệnh nhân tương đồng sinh học nhất, từ đó nội suy giá trị khuyết bằng trung vị có trọng số của các lân cận này, bảo toàn mối liên kết đa biến của hệ gen."
*   **Lời nối chuyển slide:** *"Bước tiếp theo của quy trình tiền xử lý là phát hiện các mẫu bệnh án bất thường và tiến hành chuẩn hóa quy mô dữ liệu toán học."*

---

### SLIDE 6: TIỀN XỬ LÝ DỮ LIỆU - PHẦN 2: LỌC OUTLIERS VÀ CHUẨN HÓA (Thời lượng gợi ý: 1 phút)
*   **Nội dung hiển thị:** Sơ đồ `preprocessing_logic.png`, thuật toán Isolation Forest (contamination = 0.05), phép biến đổi toán học Log1p và chuẩn hóa Robust Scaler.
*   **Kịch bản nói chi tiết:**
    > "Để loại bỏ các mẫu bệnh phẩm bị nhiễm tạp chất hoặc sai nhãn lâm sàng nghiêm trọng, chúng em sử dụng thuật toán học không giám sát **Isolation Forest** với cấu hình tỷ lệ nhiễm bẩn `contamination = 0.05`. Thuật toán sẽ cô lập các điểm dữ liệu bằng các lát cắt ngẫu nhiên trong không gian đa chiều, lọc bỏ đi 5% số mẫu bệnh nhân bất thường nhất.
    >
    > Sau khi có tập mẫu sạch, ma trận biểu hiện gen tiếp tục đi qua phép biến đổi toán học phi tuyến **Log1p**:
    >
    > $$f(x) = \ln(x + 1)$$
    > Phép biến đổi này giúp nén các dải gen biểu hiện cực mạnh vốn bị lệch phải nặng, ổn định phương sai về phân phối tiệm cận chuẩn.
    >
    > Cuối cùng là bước **Robust Scaler**: chúng em chuẩn hóa dữ liệu dựa trên trung vị (Median) và khoảng biến thiên tứ phân vị (IQR) thay vì trung bình mẫu để bảo vệ mô hình khỏi tác động của các giá trị gen đột biến cực đoan trên bệnh nhân."
*   **Lời nối chuyển slide:** *"Bên cạnh thông tin biểu hiện gen phiên mã, một nguồn thông tin vô cùng đắt giá khác là biến dị di truyền DNA cũng được tích hợp qua đường ống xử lý GATK."*

---

### SLIDE 7: TÍCH HỢP BIẾN DỊ DI TRUYỀN DNA TỪ GATK PIPELINE (Thời lượng gợi ý: 45 giây)
*   **Nội dung hiển thị:** Sơ đồ khối GATK (BAM -> HaplotypeCaller -> Mutect2 -> Funcotator), 2 biomarkers đột biến DNA nhị phân: IDH status và MGMT status.
*   **Kịch bản nói chi tiết:**
    > "Từ các tệp giải trình tự thô BAM của bệnh nhân, chúng em xây dựng pipeline **GATK v4.x** chuẩn quốc tế. Hệ thống chạy thuật toán gọi biến dị Mutect2 để phát hiện các đột biến điểm đơn nuclêôtit (SNPs) và đột biến thêm bớt đoạn nhỏ (Indels), sau đó dùng công cụ Funcotator để chú giải chức năng sinh học.
    >
    > Qua đó, chúng em trích xuất ra 2 đặc trưng di truyền nhị phân cực kỳ quan trọng được Tổ chức Y tế Thế giới (WHO) khuyến nghị:
    >
    > 1. Trạng thái đột biến **IDH1/2**: Bệnh nhân Glioma mang đột biến này thường có tiên lượng sống sót lâu hơn hẳn.
    > 2. Trạng thái promoter **MGMT**: Methyl hóa MGMT giúp vô hiệu hóa enzym sửa chữa DNA của tế bào u, khiến khối u nhạy cảm đặc biệt với hóa trị TMZ.
    >
    > Các nhãn nhị phân này được tích hợp trực tiếp vào dữ liệu đầu vào để tạo thành mô hình tiên lượng đa phương thức."
*   **Lời nối chuyển slide:** *"Sau khi hợp nhất thông tin, chiều dữ liệu vẫn còn rất lớn. Chúng em đã phát triển chiến lược lọc gen đa tầng để chiết xuất ra những gen chỉ thị tinh túy nhất."*

---

### SLIDE 8: CHIẾN LƯỢC CHỌN LỌC ĐẶC TRƯNG ĐA TẦNG (Thời lượng gợi ý: 1 phút)
*   **Nội dung hiển thị:** Phễu lọc đặc trưng qua 4 bước: Variance Filtering -> Spearman Correlation -> CoxPH L2 Regularization -> Wald Test. Danh sách biomarkers tiêu biểu.
*   **Kịch bản nói chi tiết:**
    > "Quy trình trích xuất dấu ấn sinh học được nhóm thiết kế dưới dạng phễu lọc giảm chiều thông tin nghiêm ngặt:
    >
    > *Tầng 1 (Variance Filtering):* Tính phương sai của toàn bộ gen, chỉ giữ lại Top 500 gen có mức độ biến động mạnh nhất.
    >
    > *Tầng 2 (Spearman Correlation):* Tính tương quan phi tuyến giữa biểu hiện từng gen với thời gian sinh tồn thực tế để lấy ra Top 50 gen tương quan mạnh nhất.
    >
    > *Tầng 3 (CoxPH L2 Regularization):* Huấn luyện mô hình sinh tồn CoxPH có phạt chuẩn L2 (Ridge) để loại bỏ hiện tượng đa cộng tuyến sinh ra từ các gen đồng biểu hiện thuộc cùng con đường sinh học.
    >
    > *Tầng 4 (Wald Test):* Thực hiện kiểm định Wald thống kê y học, loại bỏ các đặc trưng không có ý nghĩa thống kê thực nghiệm, giữ lại tập đặc trưng tối ưu có $p$-value < 0.05.
    >
    > Kết quả thu được bộ gen biomarkers tiêu biểu gồm: *HNRNPA1P52, ANKRD1, SCG5, RFX8, PARK7*."
*   **Lời nối chuyển slide:** *"Với bộ gen tối ưu này, mô hình đầu tiên chúng em phát triển là Ensemble LightGBM với các cải tiến kỹ thuật chống quá khớp."*

---

### SLIDE 9: MÔ HÌNH 1: ENSEMBLE LIGHTGBM - CẢI TIẾN CHỐNG OVERFITTING (Thời lượng gợi ý: 45 giây)
*   **Nội dung hiển thị:** Các siêu tham số cải tiến chống overfitting: Objective: regression/poisson, Regularization L1 & L2 lambda, Complexity Control (num_leaves = 15), Feature Fraction = 0.7.
*   **Kịch bản nói chi tiết:**
    > "LightGBM là một thuật toán học máy boosting cây quyết định cực kỳ mạnh mẽ, tuy nhiên nó rất dễ bị overfitting trên dữ liệu sinh học phân tử ít mẫu. Nhóm chúng em đã thiết lập chiến lược tinh chỉnh siêu tham số nghiêm ngặt để tối ưu hóa tính tổng quát:
    >
    > *Về hàm mục tiêu (Objective):* Thay vì dùng hồi quy MSE thông thường, chúng em cấu hình hàm lỗi `poisson` để mô hình hóa trực tiếp hàm tỷ lệ rủi ro sống sót tích lũy.
    >
    > *Về kiểm soát độ phức tạp cây:* Chúng em ép độ sâu cây quyết định rất nông bằng cách giới hạn `num_leaves = 15`. Đồng thời cấu hình `feature_fraction = 0.7` để ép mô hình chỉ lấy ngẫu nhiên 70% số gen tại mỗi lượt dựng cây, ngăn chặn việc mô hình phụ thuộc quá mức vào một vài gen nổi trội."
*   **Lời nối chuyển slide:** *"Không dừng lại ở đó, để triệt tiêu tối đa phương sai của mô hình, nhóm nghiên cứu đã áp dụng thêm cơ chế Bagging đa hạt giống ngẫu nhiên."*

---

### SLIDE 10: MÔ HÌNH 1: ENSEMBLE LIGHTGBM - BAGGING ĐA HẠT GIỐNG (Thời lượng gợi ý: 1 phút)
*   **Nội dung hiển thị:** Đồ thị `lgbm_ensemble_training_curves.png` thể hiện các đường cong RMSE của 10 hạt giống và đường trung bình đậm nét, cơ chế dừng sớm (stopping_rounds = 50).
*   **Kịch bản nói chi tiết:**
    > "Như hình vẽ trực quan hóa trên slide, nhóm chúng em thực hiện kỹ thuật **10-Seed Ensemble Bagging**. Chúng em cho huấn luyện song song 10 mô hình LightGBM con độc lập ứng với 10 hạt giống ngẫu nhiên (seed từ 42 đến 51). Điểm rủi ro sinh tồn cuối cùng của bệnh nhân sẽ là trung bình cộng đầu ra của cả 10 cây quyết định lớn này để triệt tiêu sai số cục bộ.
    >
    > Quá trình huấn luyện tích hợp cơ chế **Early Stopping**: tự động giám sát sai số RMSE trên tập kiểm chứng (Validation set), nếu liên tục trong 50 vòng lặp (`stopping_rounds=50`) sai số này không giảm thêm, mô hình con sẽ tự ngắt.
    >
    > Đường màu xanh đậm trên biểu đồ chính là giá trị trung bình tích hợp, có thể thấy nó rất mượt mà và duy trì sai số RMSE ở mức cực thấp so với bất kỳ mô hình đơn lẻ nào."
*   **Lời nối chuyển slide:** *"Bên cạnh mô hình học máy dạng cây LightGBM, nhóm chúng em đã nghiên cứu và phát triển một kiến trúc học sâu tiên tiến hơn mang tên SurvivalMambaNet. Đầu tiên là khối khử nhiễu DAE."*

---

### SLIDE 11: MÔ HÌNH 2: SURVIVALMAMBANET - KHỐI KHỬ NHIỄU DAE (Thời lượng gợi ý: 1 phút)
*   **Nội dung hiển thị:** Biểu đồ độ lỗi tái lập `dae_training_validation_loss.png`, nguyên lý DAE (Input Denoising + Gaussian Noise 0.2, Encoder phi tuyến ReLU nén dữ liệu gen 16.000+ chiều về không gian ẩn 128 chiều sạch nhiễu).
*   **Kịch bản nói chi tiết:**
    > "Dữ liệu sinh học giải trình tự gen luôn chứa các nhiễu đo đạc từ thiết bị vật lý trong phòng thí nghiệm. Để giải quyết vấn đề này, chúng em phát triển kiến trúc **Denoising Autoencoder (DAE)**.
    >
    > Cơ chế hoạt động của DAE rất đặc biệt: Chúng em cố tình thêm nhiễu Gaussian ngẫu nhiên với hệ số `0.2` vào ma trận gen đầu vào, sau đó bắt mạng nơ-ron học cách tự loại bỏ nhiễu này để tái tạo lại dữ liệu sạch ban đầu.
    >
    > Quá trình này ép mạng nơ-ron phải tìm ra các mối quan hệ cấu trúc ẩn cốt lõi của gen, nén dữ liệu từ không gian khổng lồ hơn 16.000 chiều ban đầu đi qua các tầng phi tuyến ReLU để hội tụ tại không gian ẩn **128 chiều hoàn toàn sạch nhiễu**.
    >
    > Đồ thị trên slide chứng minh độ hội tụ tuyệt vời của DAE: độ lỗi tái lập cấu trúc MSE giảm rất nhanh và tiệm cận về không trên cả tập huấn luyện lẫn tập kiểm chứng độc lập."
*   **Lời nối chuyển slide:** *"Trên không gian ẩn 128 chiều sạch nhiễu này, nhóm nghiên cứu tiếp tục tích hợp khối mô hình trạng thái chọn lọc Mamba để đưa ra tiên lượng cuối cùng."*

---

### SLIDE 12: MÔ HÌNH 2: SURVIVALMAMBANET - KHỐI MAMBA SSM & COX LOSS (Thời lượng gợi ý: 1 phút 15 giây)
*   **Nội dung hiển thị:** Hình vẽ kiến trúc `survivalmambanet_architecture.png` và đồ thị huấn luyện `survivalmambanet_training_curves.png`. Các đặc tính của Mamba (Selective Scan SSM, Cox Loss).
*   **Kịch bản nói chi tiết:**
    > "Kiến trúc mạng học sâu **SurvivalMambaNet** của chúng em là sự kết hợp giữa khối trích xuất DAE và khối **Selective State Space Model (Mamba Block)**. Khác với kiến trúc Attention của Transformer có độ phức tạp tính toán bình phương rất nặng, khối Mamba sử dụng cơ chế quét chọn lọc Selective Scan có độ phức tạp tuyến tính $O(L)$, giúp mô hình hóa các tương tác chuỗi gen dài một cách cực kỳ hiệu quả và hội tụ nhanh chóng.
    >
    > Đầu ra của mạng được huấn luyện thông qua hàm mất mát **Negative Cox Partial Likelihood Loss**. Hàm mất mát này cho phép tối ưu hóa trực tiếp thứ tự rủi ro sống sót của bệnh nhân mà không gặp trở ngại bởi hiện tượng khuyết góc dữ liệu (censored data).
    >
    > Nhìn vào biểu đồ huấn luyện bên tay phải, chúng ta thấy Cox Loss giảm sâu ổn định, đồng thời chỉ số đo lường hiệu năng C-index tăng tiệm cận lên mức rất cao, thể hiện mạng nơ-ron đã học được chính xác quy luật sinh tồn của khối u não."
*   **Lời nối chuyển slide:** *"Tiếp theo, chúng em xin trình bày kết quả thực nghiệm định lượng chi tiết thu được khi đối chiếu mô hình trên nhiều tập dữ liệu độc lập quốc tế khác nhau."*

---

### SLIDE 13: KẾT QUẢ THỰC NGHIỆM VÀ ĐỐI CHIẾU C-INDEX ĐA COHORT (Thời lượng gợi ý: 1 phút 30 giây)
*   **Nội dung hiển thị:** Biểu đồ so sánh C-index `model_comparison.png`, bảng số liệu đối chiếu trên các tập dữ liệu TCGA-LGG, CGGA-325, REMBRANDT và phân tích tích hợp đa phương thức.
*   **Kịch bản nói chi tiết:**
    > "Đây là kết quả thực nghiệm định lượng cốt lõi của nghiên cứu. Chúng em đã tiến hành kiểm chứng chéo mô hình trên nhiều đoàn hệ (cohort) độc lập để chứng minh tính thực tiễn:
    >
    > *Thứ nhất, trên tập bệnh nhân Âu-Mỹ TCGA-LGG:* Kiến trúc **SurvivalMambaNet** đạt chỉ số C-index vượt trội là **0.6742**, cao hơn đáng kể so với mô hình cải tiến LightGBM Ensemble đạt 0.6449.
    >
    > *Thứ hai, trên tập kiểm chứng chủng tộc Châu Á CGGA-325:* SurvivalMambaNet chứng minh khả năng tổng quát hóa cực kỳ mạnh mẽ khi đạt chỉ số C-index rất cao là **0.7462**.
    >
    > *Thứ ba, thách thức chuyển đổi công nghệ đo đạc REMBRANDT (Microarray):* Trong khi mô hình LightGBM Ensemble bị sập hiệu năng xuống chỉ còn 0.4503 do tác động của hiện tượng dịch chuyển phân phối công nghệ, kiến trúc học sâu SurvivalMambaNet tích hợp khối khử nhiễu DAE vẫn duy trì sự ổn định ở mức chấp nhận được là **0.5438**.
    >
    > *Thứ tư, về hiệu quả tích hợp đa phương thức (Multi-modal):* Khi chỉ sử dụng dữ liệu biểu hiện gen RNA-Seq đơn lẻ, mô hình đạt C-index là **0.5749**. Khi chúng em tích hợp thêm thông tin đột biến DNA nhị phân trích xuất từ GATK, chỉ số C-index tăng vọt lên **0.6185**, cải thiện rõ rệt +7.6% hiệu năng dự báo lâm sàng."
*   **Lời nối chuyển slide:** *"Để hiểu rõ hơn về mặt y học lâm sàng, chúng ta sẽ xem xét kết quả phân tầng sinh tồn Kaplan-Meier và phân tích giải thích tính năng thông qua SHAP."*

---

### SLIDE 14: PHÂN TẦNG SINH TỒN LÂM SÀNG & GIẢI THÍCH SHAP (Thời lượng gợi ý: 1 phút 15 giây)
*   **Nội dung hiển thị:** Biểu đồ Kaplan-Meier `km_test_cgga_325.png` và biểu đồ SHAP `shap_summary_plot.png`. Trị số p-value của kiểm định Log-rank, phân loại các gen ác tính và gen bảo vệ.
*   **Kịch bản nói chi tiết:**
    > "Biểu đồ bên trái là đường cong sống sót Kaplan-Meier phân tầng bệnh nhân trên tập CGGA-325. Đường cong màu đỏ thể hiện nhóm bệnh nhân được mô hình dự báo nguy cơ cao (High Risk), đường màu xanh thể hiện nhóm nguy cơ thấp (Low Risk). Trực quan cho thấy hai đường cong phân tách cực kỳ rõ rệt. Kiểm định giả thuyết Log-rank trả về trị số ý nghĩa thống kê cực lớn với $p\text{-value} = 1.13 \times 10^{-16}$, khẳng định mô hình phân tầng rủi ro có độ tin cậy tuyệt đối về mặt y học lâm sàng.
    >
    > Biểu đồ bên phải thể hiện phân tích đóng góp của các gen thông qua giá trị **SHAP**. 
    >
    > Các gen như **ANKRD1, SCG5, IGFBP2** được xác định là các gen ác tính (Malignant Genes): mức độ biểu hiện của chúng càng cao (màu đỏ) thì giá trị SHAP càng dương, tức là làm tăng mạnh chỉ số rủi ro nguy cơ tử vong của bệnh nhân. 
    >
    > Ngược lại, các gen như **HNRNPA1P52, MIR4280HG** được xác định là gen bảo vệ (Protective Genes): khi chúng biểu hiện mạnh thì chỉ số rủi ro sinh tồn giảm đi rõ rệt."
*   **Lời nối chuyển slide:** *"Để đưa mô hình nghiên cứu lý thuyết vào ứng dụng thực tiễn hỗ trợ bác sĩ tại bệnh viện, nhóm 6 đã đóng gói hệ thống dưới dạng một Dashboard trực tuyến."*

---

### SLIDE 15: CLINICAL DASHBOARD, BÁO CÁO CÁ NHÂN HÓA & KẾT LUẬN (Thời lượng gợi ý: 1 phút 15 giây)
*   **Nội dung hiển thị:** Hình ảnh báo cáo cá nhân hóa `patient_report_CGGA_1001.png`, tóm tắt về Streamlit Dashboard, Báo cáo tiên lượng lâm sàng cụ thể và hướng đi tương lai (MRI).
*   **Kịch bản nói chi tiết:**
    > "Chúng em đã phát triển một giao diện Web Dashboard trực quan hóa sử dụng framework **Streamlit**. Khi bác sĩ nhập thông tin biểu hiện gen và đột biến của một bệnh nhân mới, hệ thống sẽ tự động xuất ra một báo cáo tiên lượng cá nhân hóa giống như mẫu của bệnh nhân `CGGA_1001` trên màn hình:
    >
    > Bệnh nhân này có chỉ số rủi ro tích hợp rất cao là **0.84**, được xếp vào nhóm nguy cơ cao (High Risk). 
    >
    > Hệ thống đưa ra dự báo xác suất sống sót cụ thể theo thời gian: cơ hội sống sót sau 1 năm là 84%, sau 3 năm giảm còn 42%, và sau 5 năm chỉ còn 12%. 
    >
    > Bản đồ lực SHAP Force Plot giải thích chi tiết các gen đột biến cụ thể gây ra mức rủi ro này và đưa ra khuyến nghị lâm sàng tương ứng.
    >
    > **Kết luận lại:** dự án đã nghiên cứu và triển khai thành công mô hình lai kết hợp học máy và học sâu, đạt kết quả tiên lượng vượt trội. Hướng phát triển tương lai của nhóm là tích hợp thêm ảnh chụp cộng hưởng từ MRI sọ não để xây dựng mô hình đa phương thức hoàn chỉnh hơn.
    >
    > Đến đây, em xin phép kết thúc phần thuyết trình báo cáo của nhóm 6. Kính mong nhận được những câu hỏi và ý kiến đóng góp quý báu từ thầy hướng dẫn GS. TS. Lê Sỹ Vinh cùng các bạn để đề tài hoàn thiện hơn. Em xin chân thành cảm ơn!"

---
*Kịch bản này đã được thiết kế tối ưu với tổng thời gian trình bày khoảng 13 - 15 phút ở tốc độ thuyết trình tự nhiên.*
