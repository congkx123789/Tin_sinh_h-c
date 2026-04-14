import torch
import torch.nn as nn
from .mamba_block import MambaSurvivalBlock

class SurvivalMambaNet(nn.Module):
    def __init__(self, encoder, d_model, n_layers=4):
        super(SurvivalMambaNet, self).__init__()
        self.encoder = encoder # Pre-trained DAE encoder
        
        # Freeze or unfreeze encoder layers
        for param in self.encoder.parameters():
            param.requires_grad = False
            
        self.mamba_layers = nn.ModuleList([
            MambaSurvivalBlock(d_model=d_model) for _ in range(n_layers)
        ])
        
        self.survival_head = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, 1) # Output log-hazard ratio
        )

    def forward(self, x):
        # Encode gene expressions
        x = self.encoder(x)
        
        # Survival Prediction via Mamba
        # Expecting x as (batch, d_model), we might need to add a sequence dim if using Mamba
        x = x.unsqueeze(1) # (batch, 1, d_model)
        
        for layer in self.mamba_layers:
            x = layer(x)
        
        x = x.squeeze(1) # (batch, d_model)
        risk_score = self.survival_head(x)
        return risk_score
