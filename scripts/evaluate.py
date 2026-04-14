import torch
from models.survival_net import SurvivalMambaNet
from utils.metrics import concordance_index

def evaluate():
    print("Evaluating model...")
    # Load model and run on test set
    # model = SurvivalMambaNet(...)
    # model.load_state_dict(torch.load("checkpoints/mamba_weights/best_mamba.pth"))
    
    # Calculate C-index
    # c_index = concordance_index(true_times, predictions, event_observed)
    # print(f"C-index: {c_index}")
    
    print("Evaluation complete.")

if __name__ == "__main__":
    evaluate()
