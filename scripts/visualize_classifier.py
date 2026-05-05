import os
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, confusion_matrix
from lifelines import KaplanMeierFitter
from models.autoencoder import DenoisingAutoencoder
from models.survival_net import SurvivalMambaNet

def visualize_results():
    print("🎨 Generating Classification Performance Charts...")
    
    processed_dir = "data/02_processed/training/test_internal"
    results_dir = "results/classification"
    os.makedirs(results_dir, exist_ok=True)
    
    # Load Model
    input_dim = 16383
    latent_dim = 128
    ae = DenoisingAutoencoder(input_dim=input_dim, latent_dim=latent_dim)
    model = SurvivalMambaNet(encoder=ae.encoder, latent_dim=latent_dim)
    model.load_state_dict(torch.load("checkpoints/mamba_weights/best_classifier.pth"))
    model.eval()

    # Load Test Data
    X_test = pd.read_csv(os.path.join(processed_dir, "X.csv"), index_col=0)
    y_test = pd.read_csv(os.path.join(processed_dir, "y.csv"), index_col=0)
    
    true_labels = [(1 if row['OS.time'] < 365 and row['OS'] == 1 else 0) for _, row in y_test.iterrows()]
    X_tensor = torch.tensor(X_test.values, dtype=torch.float32)
    
    with torch.no_grad():
        probs = model(X_tensor, mode='classification').squeeze().numpy()
        preds = (probs > 0.5).astype(int)

    # 1. Plot Confusion Matrix
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(true_labels, preds)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Long-term', 'Short-term'], yticklabels=['Long-term', 'Short-term'])
    plt.title('Confusion Matrix - Mamba Classifier (Test Set)')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.savefig(os.path.join(results_dir, 'confusion_matrix.png'))
    plt.close()

    # 2. Plot ROC Curve
    fpr, tpr, _ = roc_curve(true_labels, probs)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) - Test Set')
    plt.legend(loc="lower right")
    plt.savefig(os.path.join(results_dir, 'roc_curve.png'))
    plt.close()

    # 3. Probability Distribution Histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(probs[np.array(true_labels) == 0], color='green', label='Long-term (Actual)', kde=True, alpha=0.5)
    sns.histplot(probs[np.array(true_labels) == 1], color='red', label='Short-term (Actual)', kde=True, alpha=0.5)
    plt.axvline(0.5, color='black', linestyle='--')
    plt.title('Distribution of Predicted Probabilities (Risk Scores)')
    plt.xlabel('Predicted Probability (Risk Score)')
    plt.ylabel('Patient Count')
    plt.legend()
    plt.savefig(os.path.join(results_dir, 'probability_distribution.png'))
    plt.close()

    # 4. Kaplan-Meier Stratification by AI Prediction
    plt.figure(figsize=(10, 7))
    kmf = KaplanMeierFitter()
    
    # High Risk (Predicted 1)
    mask_high = preds == 1
    if any(mask_high):
        kmf.fit(y_test['OS.time'][mask_high], event_observed=y_test['OS'][mask_high], label='Predicted: High Risk (Short-term)')
        kmf.plot_survival_function()
        
    # Low Risk (Predicted 0)
    mask_low = preds == 0
    if any(mask_low):
        kmf.fit(y_test['OS.time'][mask_low], event_observed=y_test['OS'][mask_low], label='Predicted: Low Risk (Long-term)')
        kmf.plot_survival_function()
        
    plt.title('Survival Curves Stratified by AI Prediction (Mamba Classifier)')
    plt.xlabel('Days')
    plt.ylabel('Survival Probability')
    plt.grid(True)
    plt.savefig(os.path.join(results_dir, 'km_stratification.png'))
    plt.close()

    print(f"✅ All charts generated in: {results_dir}")

if __name__ == "__main__":
    visualize_results()
