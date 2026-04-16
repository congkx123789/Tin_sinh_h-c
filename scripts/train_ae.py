import os
import torch
import torch.optim as optim
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
from models.autoencoder import DenoisingAutoencoder

def train():
    print("🚀 Starting Autoencoder Training...")
    
    # Load processed data
    data_dir = "data/processed"
    X_train_path = os.path.join(data_dir, "X_train.csv")
    X_val_path = os.path.join(data_dir, "X_val.csv")
    
    if not os.path.exists(X_train_path):
        print(f"❌ Error: {X_train_path} not found. Run preprocess_data.py first.")
        return

    X_train = pd.read_csv(X_train_path, index_col=0)
    X_val = pd.read_csv(X_val_path, index_col=0)
    
    input_dim = X_train.shape[1]
    latent_dim = 128
    
    # Datasets
    train_dataset = TensorDataset(torch.tensor(X_train.values, dtype=torch.float32))
    val_dataset = TensorDataset(torch.tensor(X_val.values, dtype=torch.float32))
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    
    model = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.MSELoss()
    
    epochs = 50
    noise_factor = 0.2
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for batch in train_loader:
            features = batch[0]
            noisy_features = features + noise_factor * torch.randn_like(features)
            
            optimizer.zero_grad()
            encoded, decoded = model(noisy_features)
            loss = criterion(decoded, features)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            
        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                features = batch[0]
                _, decoded = model(features)
                loss = criterion(decoded, features)
                val_loss += loss.item()
            
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss/len(train_loader):.4f}, Val Loss: {val_loss/len(val_loader):.4f}")
    
    # Save weights
    os.makedirs("checkpoints/ae_weights", exist_ok=True)
    torch.save(model.state_dict(), "checkpoints/ae_weights/best_ae.pth")
    print("✅ Autoencoder training complete. Weights saved to checkpoints/ae_weights/best_ae.pth")

if __name__ == "__main__":
    train()
