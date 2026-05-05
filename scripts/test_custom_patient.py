import os
import torch
import pandas as pd
import numpy as np
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet

def test_external_patient(dataset_path, patient_idx=0):
    print(f"🔬 Testing AI on External Data: {os.path.basename(dataset_path)}")
    print("-" * 50)
    
    # 1. Load Data
    if not os.path.exists(dataset_path):
        print(f"❌ File not found: {dataset_path}")
        return
        
    df = pd.read_csv(dataset_path, index_col=0)
    if patient_idx >= len(df):
        print(f"❌ Index {patient_idx} out of range (Total: {len(df)})")
        return
        
    patient_id = df.index[patient_idx]
    patient_data_raw = df.iloc[patient_idx:patient_idx+1]
    
    # 2. Load Model Configuration
    # We need the 16383 features used during training
    weights_path = "checkpoints/mamba_weights/best_classifier.pth"
    if not os.path.exists(weights_path):
        print("❌ Model weights not found. Train the model first.")
        return
        
    # Load Model
    input_dim = 16383 # Target features
    latent_dim = 128
    ae = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    model = SurvivalMambaNet(encoder=ae.encoder, latent_dim=latent_dim)
    model.load_state_dict(torch.load(weights_path))
    model.eval()

    # 3. Prediction
    patient_tensor = torch.tensor(patient_data_raw.values, dtype=torch.float32)
    
    with torch.no_grad():
        prob = model(patient_tensor, mode='classification').item()
        
    print(f"👤 Patient ID: {patient_id}")
    print(f"📊 Predicted Probability of Short-term survival: {prob*100:.2f}%")
    
    if prob > 0.5:
        print("\n🚩 AI PREDICTION: HIGH RISK (Short-term Survivor)")
        print("   -> Bệnh nhân có nguy cơ diễn biến nhanh, cần can thiệp tích cực.")
    else:
        print("\n✅ AI PREDICTION: LOW RISK (Long-term Survivor)")
        print("   -> Tiên lượng khả quan, đáp ứng tốt với phác đồ chuẩn.")
    print("-" * 50)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to X.csv of the external dataset")
    parser.add_argument("--idx", type=int, default=0, help="Patient index to test")
    args = parser.parse_args()
    
    test_external_patient(args.file, args.idx)
