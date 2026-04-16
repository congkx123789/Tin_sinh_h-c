import os
import torch
import torch.optim as optim
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet
from utils.loss import cox_partial_likelihood

def train():
    print("🚀 Starting Survival Mamba Training...")
    
    # Load processed data
    X_path = "data/processed/X_final.csv"
    y_path = "data/processed/y_final.csv"
    
    if not os.path.exists(X_path) or not os.path.exists(y_path):
        print(f"❌ Error: Processed data not found. Run preprocess_data.py first.")
        return

    X = pd.read_csv(X_path, index_col=0)
    y = pd.read_csv(y_path, index_col=0)
    
    input_dim = X.shape[1]
    latent_dim = 128
    
    # Pre-trained AE for initialization
    ae = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    ae_weights = "checkpoints/ae_weights/best_ae.pth"
    if os.path.exists(ae_weights):
        ae.load_state_dict(torch.load(ae_weights))
        print("Loaded pre-trained Autoencoder weights.")
    
    # Build model using AE's encoder
    model = SurvivalMambaNet(encoder=ae.encoder, d_model=latent_dim)
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    
    # Dataset
    X_tensor = torch.tensor(X.values, dtype=torch.float32)
    time_tensor = torch.tensor(y['OS.time'].values, dtype=torch.float32)
    event_tensor = torch.tensor(y['OS'].values, dtype=torch.float32)
    
    dataset = TensorDataset(X_tensor, time_tensor, event_tensor)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)
    
    epochs = 100
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for features, times, events in dataloader:
            optimizer.zero_grad()
            risk_scores = model(features).squeeze()
            loss = cox_partial_likelihood(risk_scores, times, events)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {train_loss/len(dataloader):.4f}")
            
    os.makedirs("checkpoints/mamba_weights", exist_ok=True)
    torch.save(model.state_dict(), "checkpoints/mamba_weights/best_mamba.pth")
    print("✅ Survival Mamba training complete. Weights saved to checkpoints/mamba_weights/best_mamba.pth")

if __name__ == "__main__":
    train()
