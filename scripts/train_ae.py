import os
import torch
import torch.optim as optim
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
from models.autoencoder import DenoisingAutoencoder

def train():
    print("🚀 Starting Autoencoder Training...")
    
    # Load processed data
    X_path = "data/processed/X_final.csv"
    if not os.path.exists(X_path):
        print(f"❌ Error: {X_path} not found. Run preprocess_data.py first.")
        return

    X = pd.read_csv(X_path, index_col=0)
    input_dim = X.shape[1]
    latent_dim = 128
    
    # Convert to tensor
    X_tensor = torch.tensor(X.values, dtype=torch.float32)
    dataset = TensorDataset(X_tensor)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    model = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.MSELoss()
    
    epochs = 50
    noise_factor = 0.2
    
    for epoch in range(epochs):
        train_loss = 0
        for batch in dataloader:
            features = batch[0]
            
            # Add noise for Denoising AE
            noisy_features = features + noise_factor * torch.randn_like(features)
            
            optimizer.zero_grad()
            encoded, decoded = model(noisy_features)
            loss = criterion(decoded, features)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {train_loss/len(dataloader):.4f}")
    
    # Save weights
    os.makedirs("checkpoints/ae_weights", exist_ok=True)
    torch.save(model.state_dict(), "checkpoints/ae_weights/best_ae.pth")
    print("✅ Autoencoder training complete. Weights saved to checkpoints/ae_weights/best_ae.pth")

if __name__ == "__main__":
    train()
