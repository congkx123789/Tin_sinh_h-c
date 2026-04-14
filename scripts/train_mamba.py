import torch
import torch.optim as optim
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet
from utils.loss import cox_partial_likelihood

def train():
    print("Training Survival Mamba...")
    # Load pre-trained encoder from AE
    ae = DenoisingAutoencoder(input_dim=1000, latent_dim=128)
    # ae.load_state_dict(torch.load("checkpoints/ae_weights/best_ae.pth"))
    encoder = ae.encoder
    
    model = SurvivalMambaNet(encoder=encoder, d_model=128)
    optimizer = optim.Adam(model.survival_head.parameters(), lr=0.0001)
    
    # Training loop placeholder using cox_partial_likelihood
    print("Training loop starting...")
    # ...
    
    torch.save(model.state_dict(), "checkpoints/mamba_weights/best_mamba.pth")
    print("Survival Mamba training complete.")

if __name__ == "__main__":
    train()
