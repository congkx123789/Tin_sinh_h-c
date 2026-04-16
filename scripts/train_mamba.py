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
    data_dir = "data/processed"
    X_train_path = os.path.join(data_dir, "X_train.csv")
    y_train_path = os.path.join(data_dir, "y_train.csv")
    X_val_path = os.path.join(data_dir, "X_val.csv")
    y_val_path = os.path.join(data_dir, "y_val.csv")
    
    if not (os.path.exists(X_train_path) and os.path.exists(y_train_path)):
        print(f"❌ Error: Processed data not found. Run preprocess_data.py first.")
        return

    X_train = pd.read_csv(X_train_path, index_col=0)
    y_train = pd.read_csv(y_train_path, index_col=0)
    X_val = pd.read_csv(X_val_path, index_col=0)
    y_val = pd.read_csv(y_val_path, index_col=0)
    
    input_dim = X_train.shape[1]
    latent_dim = 128
    
    # Pre-trained AE for initialization
    ae = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    ae_weights = "checkpoints/ae_weights/best_ae.pth"
    if os.path.exists(ae_weights):
        ae.load_state_dict(torch.load(ae_weights))
        print("✅ Loaded pre-trained Autoencoder weights.")
    
    # Build model using AE's encoder
    model = SurvivalMambaNet(encoder=ae.encoder, latent_dim=latent_dim)
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    
    # Datasets
    X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
    time_train = torch.tensor(y_train['OS.time'].values, dtype=torch.float32)
    event_train = torch.tensor(y_train['OS'].values, dtype=torch.float32)
    
    train_dataset = TensorDataset(X_train_tensor, time_train, event_train)
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    
    # Validation Tensors
    X_val_tensor = torch.tensor(X_val.values, dtype=torch.float32)
    time_val = torch.tensor(y_val['OS.time'].values, dtype=torch.float32)
    event_val = torch.tensor(y_val['OS'].values, dtype=torch.float32)
    
    epochs = 100
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for features, times, events in train_loader:
            optimizer.zero_grad()
            risk_scores = model(features).squeeze()
            loss = cox_partial_likelihood(risk_scores, times, events)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            
        # Validation Loss
        model.eval()
        with torch.no_grad():
            val_risk_scores = model(X_val_tensor).squeeze()
            val_loss = cox_partial_likelihood(val_risk_scores, time_val, event_val)
            
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss/len(train_loader):.4f}, Val Loss: {val_loss.item():.4f}")
            
    os.makedirs("checkpoints/mamba_weights", exist_ok=True)
    torch.save(model.state_dict(), "checkpoints/mamba_weights/best_mamba.pth")
    print("✅ Survival Mamba training complete. Weights saved to checkpoints/mamba_weights/best_mamba.pth")

if __name__ == "__main__":
    train()
