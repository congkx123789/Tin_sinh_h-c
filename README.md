# 🧬 GBM Survival Prediction using Mamba-SSM

Mô hình học sâu tiên tiến sử dụng kiến trúc **Mamba (Selective State Space Model)** để dự đoán tiên lượng sống sót của bệnh nhân u não (Glioblastoma) dựa trên dữ liệu biểu hiện gen (16,504 gen).

## 🚀 Hướng dẫn bắt đầu nhanh (Quick Start)

### 1. Cài đặt môi trường
```bash
conda create -n mamba_env python=3.10
conda activate mamba_env
pip install -r requirements.txt
```

### 2. Khôi phục dữ liệu (Bắt buộc nếu tải từ GitHub)
Dữ liệu lớn (>100MB) đã được chia nhỏ để phù hợp với GitHub. Chạy script sau để khôi phục tệp gốc:
```bash
bash scripts/reconstruct_data.sh
```

### 3. Đánh giá mô hình (Validation)
Sử dụng các trọng số đã huấn luyện (trong `checkpoints/`) để kiểm chứng trên từng bộ dữ liệu:
```bash
python scripts/evaluate.py [split_name]
# Ví dụ: python scripts/evaluate.py test_cgga_325
```

## 🎯 Kết quả Thực nghiệm (C-index)

Chúng tôi đã thực hiện quy trình kiểm chứng ngoại kiểm đa trung tâm (Multi-center Validation) với kết quả rất ổn định:

| Nguồn dữ liệu | Số mẫu | Nền tảng | C-index |
| :--- | :--- | :--- | :--- |
| **TCGA-GBM** (Internal) | 150+ | RNA-Seq | **0.6151** |
| **TCGA-LGG** (External) | 500+ | RNA-Seq | **0.6569** 🚀 |
| **CGGA-325** | 325 | RNA-Seq | **0.6325** |
| **CGGA-693** | 693 | RNA-Seq | **0.5793** |
| **GSE4412** | 85 | Microarray | **0.5801** |
| **GSE13041** | 191 | Microarray | **0.5478** |
| **REMBRANDT** | 490 | Microarray | **0.4582** |

## 🌐 Nguồn dữ liệu gốc (Detailed Data Sources)

Toàn bộ dữ liệu được thu thập từ các cổng thông tin Sinh tin học chính thống quốc tế:

1.  **TCGA (The Cancer Genome Atlas)**: [GDC Cancer Portal](https://portal.gdc.cancer.gov/) - Dữ liệu GBM và LGG từ Hoa Kỳ.
2.  **CGGA (Chinese Glioma Genome Atlas)**: [CGGA Website](http://www.cgga.org.cn/) - Dữ liệu bệnh nhân khu vực Châu Á.
3.  **NCBI GEO (Gene Expression Omnibus)**:
    - [GSE108476 (REMBRANDT)](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE108476)
    - [GSE4271 (Phillips et al.)](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4271)
    - [GSE7696 (Sun et al.)](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE7696)
    - [GSE13041 (Lee et al.)](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE13041)
    - [GSE4412 (Freije et al.)](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4412)

## 📂 Sơ đồ tổ chức thư mục (Data Architecture)
```text
data/
├── 01_raw/          # Dữ liệu gốc (TCGA, CGGA, GEO)
├── 02_processed/    # Dữ liệu sạch (Training & Validation)
└── 03_metadata/     # Bảng ánh xạ Gen & ID probe
```
*Chi tiết các file đã split xem tại [data/DATA_MAP.md](./data/DATA_MAP.md).*

---
**Dự án được phát triển bởi AI Agent với sự cố vấn chuyên môn nghiên cứu.**
