import os
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet
from utils.metrics import calculate_km_curve

def analyze_treatment():
    print("🚀 Starting Treatment Response Analysis...")
    
    data_dir = "data/02_processed/training/train" # Using train set for more data points to plot treatment
    X_path = os.path.join(data_dir, "X.csv")
    y_path = os.path.join(data_dir, "y.csv")
    
    if not os.path.exists(X_path):
        print("❌ Error: Test data not found. Run preprocess_data.py first.")
        return
        
    X_df = pd.read_csv(X_path, index_col=0)
    y_df = pd.read_csv(y_path, index_col=0)
    
    if 'Treatment' not in y_df.columns:
        print("❌ Error: 'Treatment' column not found in y.csv. Did you run the updated preprocess_data.py?")
        return
        
    # Reconstruct Model
    input_dim = X_df.shape[1]
    latent_dim = 128
    
    ae = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    model = SurvivalMambaNet(encoder=ae.encoder, latent_dim=latent_dim)
    
    # Load Weights
    mamba_weights = "checkpoints/mamba_weights/best_mamba.pth"
    if os.path.exists(mamba_weights):
        model.load_state_dict(torch.load(mamba_weights))
        print("✅ Loaded model weights.")
    else:
        print("❌ Error: Model weights not found. Train the model first.")
        return
        
    model.eval()
    
    # Predict Risk Scores
    X_tensor = torch.tensor(X_df.values, dtype=torch.float32)
    with torch.no_grad():
        risk_scores = model(X_tensor).squeeze().numpy()
        
    times = y_df['OS.time'].values
    events = y_df['OS'].values
    treatments = y_df['Treatment'].values
    
    median_risk = np.median(risk_scores)
    high_risk_mask = (risk_scores >= median_risk)
    low_risk_mask = ~high_risk_mask
    
    treated_mask = np.isin(treatments, ['Chemo+Radiation', 'Radiation', 'Chemotherapy'])
    untreated_mask = ~treated_mask
    
    plt.figure(figsize=(12, 8))
    
    # 1. High Risk + Treated
    mask1 = high_risk_mask & treated_mask
    if sum(mask1) > 0:
        t1, s1 = calculate_km_curve(times[mask1], events[mask1])
        plt.step(t1, s1, where='post', label=f'High Risk + Treated (N={sum(mask1)})', color='darkred', linestyle='-')
        
    # 2. High Risk + Untreated
    mask2 = high_risk_mask & untreated_mask
    if sum(mask2) > 0:
        t2, s2 = calculate_km_curve(times[mask2], events[mask2])
        plt.step(t2, s2, where='post', label=f'High Risk + Untreated (N={sum(mask2)})', color='salmon', linestyle='--')
        
    # 3. Low Risk + Treated
    mask3 = low_risk_mask & treated_mask
    if sum(mask3) > 0:
        t3, s3 = calculate_km_curve(times[mask3], events[mask3])
        plt.step(t3, s3, where='post', label=f'Low Risk + Treated (N={sum(mask3)})', color='darkblue', linestyle='-')
        
    # 4. Low Risk + Untreated
    mask4 = low_risk_mask & untreated_mask
    if sum(mask4) > 0:
        t4, s4 = calculate_km_curve(times[mask4], events[mask4])
        plt.step(t4, s4, where='post', label=f'Low Risk + Untreated (N={sum(mask4)})', color='skyblue', linestyle='--')
        
    plt.title("Kaplan-Meier Survival Curves Stratified by Risk and Treatment")
    plt.xlabel("Survival Time (Days)")
    plt.ylabel("Survival Probability")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    os.makedirs("results", exist_ok=True)
    plot_path = "results/treatment_km_plot.png"
    plt.savefig(plot_path)
    print(f"✅ Treatment evaluation complete. Plot saved to {plot_path}")

if __name__ == "__main__":
    analyze_treatment()
