import os
import pandas as pd
from utils.preprocessing import RNASeqCleaner

def sync_validation_data():
    print("🚀 Starting Batch Synchronization of Validation Data...")
    
    val_dir = "data/02_processed/validation"
    scaler_path = "data/02_processed/training/scaler.pkl"
    
    if not os.path.exists(scaler_path):
        print("❌ Error: scaler.pkl not found. Run preprocess_data.py first to generate the training state.")
        return
        
    # Load cleaner state
    cleaner = RNASeqCleaner()
    cleaner.load_state(scaler_path)
    print(f"✅ Loaded cleaner state with {len(cleaner.features)} target features.")
    
    if not os.path.exists(val_dir):
        print(f"Directory {val_dir} does not exist.")
        return
        
    # Find all validation subdirectories
    subdirs = [d for d in os.listdir(val_dir) if os.path.isdir(os.path.join(val_dir, d))]
    
    for d in subdirs:
        print(f"\n--- Syncing dataset: {d} ---")
        x_path = os.path.join(val_dir, d, "X.csv")
        
        if not os.path.exists(x_path):
            print(f"Skipping {d}: X.csv not found.")
            continue
            
        print(f"Loading {x_path}...")
        df_val = pd.read_csv(x_path, index_col=0)
        print(f"Original shape: {df_val.shape}")
        
        # Apply transformation
        try:
            df_val_synced = cleaner.transform(df_val)
            print(f"Synced shape: {df_val_synced.shape}")
            
            # Overwrite X.csv
            df_val_synced.to_csv(x_path)
            print(f"✅ Successfully updated {x_path}")
        except Exception as e:
            print(f"❌ Error syncing {d}: {e}")

    print("\n✅ All validation datasets synchronized.")

if __name__ == "__main__":
    sync_validation_data()
