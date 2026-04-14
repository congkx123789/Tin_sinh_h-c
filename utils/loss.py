import torch

def cox_partial_likelihood(outputs, targets, events):
    """
    targets: survival time
    events: status (1 for death, 0 for censored)
    outputs: predicted risk score
    """
    # Sort by survival time descending
    indices = torch.argsort(targets, descending=True)
    events = events[indices]
    outputs = outputs[indices]
    
    exp_h = torch.exp(outputs)
    cumsum_exp_h = torch.cumsum(exp_h, dim=0)
    
    # Negative log partial likelihood
    log_likelihood = torch.sum(events * (outputs - torch.log(cumsum_exp_h)))
    return -log_likelihood / torch.sum(events)
