import os
from huggingface_hub import snapshot_download

def download_data():
    repo_id = "Cong123779/gbm_survival_data"
    local_dir = "data"
    
    print(f"🚀 Initializing data synchronization from Hugging Face: {repo_id}")
    
    try:
        # Create data directory if it doesn't exist
        os.makedirs(local_dir, exist_ok=True)
        
        # Download the snapshot to the local data directory
        # This will only download files that are missing or changed
        snapshot_download(
            repo_id=repo_id,
            repo_type="dataset",
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        
        print(f"✅ Data synchronization complete! All files are in '{local_dir}/'")
        
    except Exception as e:
        print(f"❌ Error during download: {e}")
        print("Please ensure you have internet access and the repository is public or you are logged in.")

if __name__ == "__main__":
    download_data()
