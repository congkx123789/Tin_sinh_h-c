import os
import requests
from tqdm import tqdm

def download_file(url, dest_path):
    print(f"Downloading {url} to {dest_path}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "wb") as f, tqdm(
        desc=os.path.basename(dest_path),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)

def main():
    base_url = "https://gdc-hub.s3.us-east-1.amazonaws.com/download/"
    files = {
        "TCGA-GBM.star_fpkm.tsv.gz": "data/raw/gbm_rna_seq.tsv.gz",
        "TCGA-GBM.clinical.tsv.gz": "data/raw/gbm_clinical.tsv.gz",
        "TCGA-GBM.survival.tsv.gz": "data/raw/gbm_survival.tsv.gz",
        "gencode.v22.annotation.gene.probeMap": "data/raw/gencode_probemap.tsv"
    }
    
    for filename, dest in files.items():
        url = base_url + filename
        if not os.path.exists(dest):
            download_file(url, dest)
        else:
            print(f"File {dest} already exists, skipping.")

    print("\nAll downloads complete! Files are in data/raw/")

if __name__ == "__main__":
    main()
