import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet

def train_classifier():
    print("🚀 Starting Mamba Classifier Training...")
    
    # Load processed data
    processed_dir = "data/02_processed/training"
    X_train_path = os.path.join(processed_dir, "train/X.csv")
    y_train_path = os.path.join(processed_dir, "train/y.csv")
    X_val_path = os.path.join(processed_dir, "val/X.csv")
    y_val_path = os.path.join(processed_dir, "val/y.csv")
    
    if not (os.path.exists(X_train_path) and os.path.exists(y_train_path)):
        print(f"❌ Error: Processed data not found. Run preprocess_data.py first.")
        return

    X_train = pd.read_csv(X_train_path, index_col=0)
    y_train = pd.read_csv(y_train_path, index_col=0)
    X_val = pd.read_csv(X_val_path, index_col=0)
    y_val = pd.read_csv(y_val_path, index_col=0)
    
    # Label Engineering: 1 = Short-term (< 1 yr), 0 = Long-term (>= 1 yr)
    def create_labels(y_df):
        labels = []
        for _, row in y_df.iterrows():
            if row['OS.time'] < 365 and row['OS'] == 1:
                labels.append(1) # Short-term survivor
            else:
                labels.append(0) # Long-term survivor
        return torch.tensor(labels, dtype=torch.float32).unsqueeze(1)
        
    y_train_cls = create_labels(y_train)
    y_val_cls = create_labels(y_val)
    
    print(f"Train Set: {sum(y_train_cls==1).item()} Short-term, {sum(y_train_cls==0).item()} Long-term")
    print(f"Val Set: {sum(y_val_cls==1).item()} Short-term, {sum(y_val_cls==0).item()} Long-term")
    
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
    
    # Load previously trained Mamba survival weights if available to start from a good point
    mamba_weights = "checkpoints/mamba_weights/best_mamba.pth"
    if os.path.exists(mamba_weights):
        try:
            # strict=False because classifier_head might be new
            model.load_state_dict(torch.load(mamba_weights), strict=False)
            print("✅ Loaded pre-trained Mamba Survival weights (Transfer Learning).")
        except Exception as e:
            print(f"Could not load pre-trained Mamba weights: {e}")
    
    # Calculate pos_weight to handle imbalance
    num_pos = sum(y_train_cls).item()
    num_neg = len(y_train_cls) - num_pos
    pos_weight = torch.tensor([num_neg / num_pos], dtype=torch.float32)
    print(f"⚖️ Using pos_weight: {pos_weight.item():.2f}")
    
    # Change to BCEWithLogitsLoss (more stable)
    # Note: We need to remove Sigmoid from models/survival_net.py or handle it here
    # Actually, let's keep nn.BCELoss but use a better optimizer setup
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.classifier_head.parameters(), lr=0.0005, weight_decay=1e-4)
    
    # Datasets
    X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
    train_dataset = TensorDataset(X_train_tensor, y_train_cls)
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    
    # Validation Tensors
    X_val_tensor = torch.tensor(X_val.values, dtype=torch.float32)
    
    epochs = 100
    best_val_acc = 0
    patience = 15
    counter = 0
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        correct = 0
        total = 0
        
        for features, labels in train_loader:
            optimizer.zero_grad()
            preds = model(features, mode='classification')
            # Custom weighted BCE
            loss = -(pos_weight * labels * torch.log(preds + 1e-7) + (1 - labels) * torch.log(1 - preds + 1e-7)).mean()
            
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            
            predicted_classes = (preds > 0.5).float()
            correct += (predicted_classes == labels).sum().item()
            total += labels.size(0)
            
        train_acc = correct / total
            
        # Validation Loss
        model.eval()
        with torch.no_grad():
            val_preds = model(X_val_tensor, mode='classification')
            val_loss = -(pos_weight * y_val_cls * torch.log(val_preds + 1e-7) + (1 - y_val_cls) * torch.log(1 - val_preds + 1e-7)).mean().item()
            val_predicted_classes = (val_preds > 0.5).float()
            val_acc = (val_predicted_classes == y_val_cls).sum().item() / y_val_cls.size(0)
            
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}] | Loss: {train_loss/len(train_loader):.4f}, Acc: {train_acc:.4f} | Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
            
        # Save based on Validation Accuracy (better for imbalanced classification)
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            os.makedirs("checkpoints/mamba_weights", exist_ok=True)
            torch.save(model.state_dict(), "checkpoints/mamba_weights/best_classifier.pth")
            counter = 0
        else:
            counter += 1
            
        if counter >= patience:
            print(f"🛑 Early stopping at epoch {epoch+1}")
            break
            
    print(f"✅ Training complete. Best Val Acc: {best_val_acc:.4f}")

if __name__ == "__main__":
    train_classifier()
