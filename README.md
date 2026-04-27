# 🧬 GBM Survival Prediction using Mamba-SSM

Mô hình học sâu sử dụng kiến trúc **Mamba (Selective State Space Model)** để dự đoán tiên lượng sống sót của bệnh nhân u não (GBM) từ dữ liệu biểu hiện gen (16,504 gen).

## 🎯 Kết quả Kiểm chứng (C-index)

Mô hình được thử nghiệm trên hàng ngàn mẫu bệnh nhân từ nhiều nguồn quốc tế:

| Nguồn dữ liệu | Nền tảng | Số mẫu | C-index |
| :--- | :--- | :--- | :--- |
| **TCGA-GBM** (Internal) | RNA-Seq | 150+ | **0.6151** |
| **TCGA-LGG** (External) | RNA-Seq | 500+ | **0.6569** 🚀 |
| **CGGA-325** | RNA-Seq | 325 | **0.6325** |
| **CGGA-693** | RNA-Seq | 693 | **0.5793** |
| **GSE4412** | Microarray | 85 | **0.5801** |
| **GSE13041** | Microarray | 191 | **0.5478** |
| **REMBRANDT** | Microarray | 490 | **0.4582** |

## 📂 Cấu trúc Dữ liệu (New Architecture)
```text
data/
├── 01_raw/          # Dữ liệu gốc (TCGA, CGGA, GEO)
├── 02_processed/    # Dữ liệu sạch (Training & Validation)
└── 03_metadata/     # Bảng ánh xạ Gen & ID
```

## 🚀 Cách chạy nhanh
1. **Huấn luyện**:
   ```bash
   python scripts/train_ae.py
   python scripts/train_mamba.py
   ```
2. **Đánh giá**:
   ```bash
   python scripts/evaluate.py [split_name]
   # Ví dụ: python scripts/evaluate.py test_cgga_325
   ```

## 🛠 Tính năng mới
- Tự động ánh xạ Gene Symbol từ Probe ID (MyGene API).
- Tự động nhận diện Log-scale trong tiền xử lý.
- Quy hoạch dữ liệu phân cấp đạt chuẩn nghiên cứu.

## 🌐 Nguồn dữ liệu (Data Sources)
1. **TCGA (The Cancer Genome Atlas)**: [GDC Portal](https://portal.gdc.cancer.gov/)
2. **CGGA (Chinese Glioma Genome Atlas)**: [CGGA Website](http://www.cgga.org.cn/)
3. **GEO (NCBI Gene Expression Omnibus)**:
   - [GSE108476](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE108476) (REMBRANDT Project)
   - [GSE4271](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4271) (Phillips et al.)
   - [GSE7696](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE7696) (Sun et al.)
   - [GSE13041](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE13041) (Lee et al.)
   - [GSE4412](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4412) (Freije et al.)

---
**Project phát triển bởi AI Agent & Chuyên gia.**
