import torch
import torch.nn as nn
from .mamba_block import MambaSurvivalBlock

class SurvivalMambaNet(nn.Module):
    def __init__(self, encoder, latent_dim=128, num_tokens=8, n_layers=4):
        super(SurvivalMambaNet, self).__init__()
        self.encoder = encoder # Pre-trained DAE encoder
        self.num_tokens = num_tokens
        self.token_dim = latent_dim // num_tokens
        
        # Freeze or unfreeze encoder layers
        for param in self.encoder.parameters():
            param.requires_grad = False
            
        self.mamba_layers = nn.ModuleList([
            MambaSurvivalBlock(d_model=self.token_dim) for _ in range(n_layers)
        ])
        
        self.survival_head = nn.Sequential(
            nn.Linear(self.token_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1) # Output log-hazard ratio
        )

    def forward(self, x):
        # Encode gene expressions
        latent = self.encoder(x) # (batch, 128)
        
        # Reshape to sequence: (batch, num_tokens, token_dim)
        # e.g. (batch, 128) -> (batch, 8, 16)
        x = latent.view(latent.size(0), self.num_tokens, self.token_dim)
        
        for layer in self.mamba_layers:
            x = layer(x)
        
        # Global Average Pooling (Mean over tokens)
        x = x.mean(dim=1) # (batch, token_dim)
        
        risk_score = self.survival_head(x)
        return risk_score
