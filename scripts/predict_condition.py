import os
import torch
import pandas as pd
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet

def predict_patient_condition(patient_index=0, dataset="test_internal"):
    print(f"🏥 Clinical AI System: Patient Condition Prediction")
    print(f"--------------------------------------------------")
    
    # Load dataset
    data_path = f"data/02_processed/training/{dataset}/X.csv"
    if not os.path.exists(data_path):
        print(f"❌ Error: Dataset {dataset} not found at {data_path}")
        return
        
    X_df = pd.read_csv(data_path, index_col=0)
    
    if patient_index >= len(X_df):
        print(f"❌ Error: Patient index out of range. Max index: {len(X_df)-1}")
        return
        
    patient_id = X_df.index[patient_index]
    patient_data = torch.tensor(X_df.iloc[patient_index].values, dtype=torch.float32).unsqueeze(0)
    
    print(f"👤 Patient ID: {patient_id}")
    
    # Load Models
    input_dim = X_df.shape[1]
    latent_dim = 128
    
    ae = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    model = SurvivalMambaNet(encoder=ae.encoder, latent_dim=latent_dim)
    
    weights_path = "checkpoints/mamba_weights/best_classifier.pth"
    if not os.path.exists(weights_path):
        print("❌ Error: Classifier weights not found. Run train_classifier.py first.")
        return
        
    model.load_state_dict(torch.load(weights_path))
    model.eval()
    
    with torch.no_grad():
        # Predict probability of being short-term survivor
        prob = model(patient_data, mode='classification').item()
        
    print(f"\n📊 AI Analysis Report:")
    print(f"   Probability of Short-term Survival (< 1 Year): {prob * 100:.2f}%")
    
    if prob > 0.6:
        print(f"\n⚠️  DIAGNOSIS: Tiên lượng Rất Xấu (High-Risk Patient)")
        print(f"   Bệnh nhân có nguy cơ cao tử vong trong vòng 1 năm.")
        print(f"   Khuyến nghị Y khoa: Cần phác đồ điều trị tích cực ngay lập tức (Chemo+Radiation).")
    elif prob > 0.4:
        print(f"\n⚠️  DIAGNOSIS: Tiên lượng Trung bình (Medium-Risk Patient)")
        print(f"   Bệnh nhân ở ngưỡng rủi ro, cần theo dõi sát sao.")
    else:
        print(f"\n✅ DIAGNOSIS: Tiên lượng Khả quan (Low-Risk Patient)")
        print(f"   Bệnh nhân có khả năng sống sót tốt qua 1 năm.")
        print(f"   Khuyến nghị Y khoa: Phác đồ chuẩn.")
        
    print(f"--------------------------------------------------")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--idx", type=int, default=0, help="Patient index in the dataset")
    parser.add_argument("--dataset", type=str, default="test_internal", help="Dataset name (test_internal, test_lgg, etc.)")
    args = parser.parse_args()
    
    predict_patient_condition(patient_index=args.idx, dataset=args.dataset)
