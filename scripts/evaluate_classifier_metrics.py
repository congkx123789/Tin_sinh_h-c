import os
import torch
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet

def evaluate_metrics():
    print("📊 Evaluating Mamba Classifier Performance...")
    print("-" * 50)
    
    processed_dir = "data/02_processed/training"
    sets = ["train", "val", "test_internal"]
    
    # Load Model
    input_dim = 16383 # From previous run
    latent_dim = 128
    ae = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    model = SurvivalMambaNet(encoder=ae.encoder, latent_dim=latent_dim)
    
    weights_path = "checkpoints/mamba_weights/best_classifier.pth"
    if not os.path.exists(weights_path):
        print("❌ Error: Classifier weights not found.")
        return
    model.load_state_dict(torch.load(weights_path))
    model.eval()

    def get_labels(y_df):
        return [(1 if row['OS.time'] < 365 and row['OS'] == 1 else 0) for _, row in y_df.iterrows()]

    results = {}
    
    for s in sets:
        x_path = os.path.join(processed_dir, s, "X.csv")
        y_path = os.path.join(processed_dir, s, "y.csv")
        
        if not os.path.exists(x_path): continue
        
        X = pd.read_csv(x_path, index_col=0)
        y = pd.read_csv(y_path, index_col=0)
        
        true_labels = get_labels(y)
        X_tensor = torch.tensor(X.values, dtype=torch.float32)
        
        with torch.no_grad():
            probs = model(X_tensor, mode='classification').squeeze().numpy()
            preds = (probs > 0.5).astype(int)
        
        acc = accuracy_score(true_labels, preds)
        results[s] = {
            "accuracy": acc,
            "report": classification_report(true_labels, preds, target_names=["Long-term", "Short-term"], output_dict=True),
            "cm": confusion_matrix(true_labels, preds)
        }
        
        print(f"\n📈 Results for [{s.upper()}] set:")
        print(f"   Accuracy: {acc:.4f}")
        print(f"   Precision (Short-term): {results[s]['report']['Short-term']['precision']:.4f}")
        print(f"   Recall (Short-term): {results[s]['report']['Short-term']['recall']:.4f}")
        print(f"   F1-Score (Short-term): {results[s]['report']['Short-term']['f1-score']:.4f}")
        print(f"   Confusion Matrix:\n{results[s]['cm']}")

    print("-" * 50)
    print("✅ Evaluation complete.")

if __name__ == "__main__":
    evaluate_metrics()
