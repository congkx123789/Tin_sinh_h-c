import numpy as np

def concordance_index(event_times, predicted_scores, event_observed):
    """
    Native implementation of C-index to avoid lifelines dependency.
    event_times: array of survival times
    predicted_scores: array of risk scores (higher means higher risk)
    event_observed: array of event markers (1 if event happened, 0 if censored)
    """
    n = len(event_times)
    count = 0
    total = 0
    
    for i in range(n):
        if event_observed[i] == 1:
            for j in range(n):
                if event_times[j] > event_times[i]:
                    total += 1
                    if predicted_scores[i] > predicted_scores[j]:
                        count += 1
                    elif predicted_scores[i] == predicted_scores[j]:
                        count += 0.5
    
    return count / total if total > 0 else 0.5

def calculate_km_curve(times, events):
    """
    Native Kaplan-Meier estimate implementation.
    """
    idx = np.argsort(times)
    times = times[idx]
    events = events[idx]
    
    unique_times = np.unique(times)
    survival_probs = [1.0]
    timeline = [0.0]
    
    current_surv = 1.0
    n_at_risk = len(times)
    
    for t in unique_times:
        n_events = np.sum(events[times == t])
        n_censored = np.sum((events == 0) & (times == t))
        
        if n_at_risk > 0:
            current_surv *= (1.0 - n_events / n_at_risk)
        
        timeline.append(t)
        survival_probs.append(current_surv)
        
        n_at_risk -= (n_events + n_censored)
        
    return np.array(timeline), np.array(survival_probs)
