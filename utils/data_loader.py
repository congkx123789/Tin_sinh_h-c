import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np

class SurvivalDataset(Dataset):
    def __init__(self, gene_path, clinical_path):
        self.gene_data = pd.read_csv(gene_path)
        self.clinical_data = pd.read_csv(clinical_path)
        
        # Merge and align data here
        # For now, placeholder for features, time, and event
        self.features = torch.tensor(self.gene_data.values, dtype=torch.float32)
        self.time = torch.tensor(self.clinical_data['OS.time'].values, dtype=torch.float32)
        self.event = torch.tensor(self.clinical_data['OS'].values, dtype=torch.float32)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.time[idx], self.event[idx]
