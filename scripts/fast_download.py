import os
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def download_chunk(url, start, end, chunk_id, dest_folder):
    headers = {'Range': f'bytes={start}-{end}'}
    r = requests.get(url, headers=headers, stream=True)
    chunk_file = os.path.join(dest_folder, f"chunk_{chunk_id}")
    with open(chunk_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
    return chunk_file

def fast_download(url, filename, num_threads=8):
    response = requests.head(url, allow_redirects=True)
    file_size = int(response.headers.get('content-length', 0))
    
    if file_size == 0:
        print("Server did not return content-length. Falling back to normal download.")
        r = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                f.write(chunk)
        return

    print(f"File size: {file_size / (1024*1024):.2f} MB")
    chunk_size = file_size // num_threads
    dest_folder = "temp_chunks"
    os.makedirs(dest_folder, exist_ok=True)

    futures = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            start = i * chunk_size
            end = i * chunk_size + chunk_size - 1 if i < num_threads - 1 else file_size - 1
            futures.append(executor.submit(download_chunk, url, start, end, i, dest_folder))

    with open(filename, 'wb') as final_file:
        for i in range(num_threads):
            chunk_file = os.path.join(dest_folder, f"chunk_{i}")
            with open(chunk_file, 'rb') as f:
                final_file.write(f.read())
            os.remove(chunk_file)
    
    os.rmdir(dest_folder)
    print(f"✅ Fast download completed: {filename}")

if __name__ == "__main__":
    # Test link from a fast CDN (Georgetown database or similar)
    target_url = "https://raw.githubusercontent.com/state-spaces/mamba/main/README.md"
    fast_download(target_url, "test_download.md")
