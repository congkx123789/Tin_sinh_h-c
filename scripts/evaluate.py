import os
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet
from utils.metrics import concordance_index, calculate_km_curve

def evaluate(data_split="test_internal"):
    print(f"🚀 Starting Evaluation on {data_split}...")
    
    # 1. Load Data
    data_dir = os.path.join("data/processed", data_split)
    X_test_path = os.path.join(data_dir, "X.csv")
    y_test_path = os.path.join(data_dir, "y.csv")
    
    if not os.path.exists(X_test_path):
        print("❌ Error: Test data not found. Run preprocess_data.py first.")
        return
        
    X_test_df = pd.read_csv(X_test_path, index_col=0)
    y_test_df = pd.read_csv(y_test_path, index_col=0)
    
    # 2. Reconstruct Model
    input_dim = X_test_df.shape[1]
    latent_dim = 128
    
    ae = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    model = SurvivalMambaNet(encoder=ae.encoder, latent_dim=latent_dim)
    
    # 3. Load Weights
    mamba_weights = "checkpoints/mamba_weights/best_mamba.pth"
    if os.path.exists(mamba_weights):
        model.load_state_dict(torch.load(mamba_weights))
        print("✅ Loaded model weights.")
    else:
        print("❌ Error: Model weights not found.")
        return
        
    model.eval()
    
    # 4. Predict Risk Scores
    X_tensor = torch.tensor(X_test_df.values, dtype=torch.float32)
    with torch.no_grad():
        risk_scores = model(X_tensor).squeeze().numpy()
        
    # 5. Calculate C-Index
    times = y_test_df['OS.time'].values
    events = y_test_df['OS'].values
    
    c_index = concordance_index(times, risk_scores, events)
    print(f"🔥 Test C-index: {c_index:.4f}")
    
    # 6. Kaplan-Meier Visualization
    median_risk = np.median(risk_scores)
    high_risk_mask = (risk_scores >= median_risk)
    low_risk_mask = ~high_risk_mask
    
    plt.figure(figsize=(10, 6))
    
    # Low Risk Plot
    t_low, s_low = calculate_km_curve(times[low_risk_mask], events[low_risk_mask])
    plt.step(t_low, s_low, where='post', label=f'Low Risk (N={sum(low_risk_mask)})', color='blue')
    
    # High Risk Plot
    t_high, s_high = calculate_km_curve(times[high_risk_mask], events[high_risk_mask])
    plt.step(t_high, s_high, where='post', label=f'High Risk (N={sum(high_risk_mask)})', color='red')
    
    plt.title("Kaplan-Meier Survival Curves (TCGA-GBM Test Set)")
    plt.xlabel("Survival Time (Days)")
    plt.ylabel("Survival Probability")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Save Plot
    os.makedirs("results", exist_ok=True)
    plot_path = f"results/km_plot_{data_split}.png"
    plt.savefig(plot_path)
    print(f"✅ Evaluation complete. Kaplan-Meier plot saved to {plot_path}")

if __name__ == "__main__":
    import sys
    split = sys.argv[1] if len(sys.argv) > 1 else "test_internal"
    evaluate(split)
