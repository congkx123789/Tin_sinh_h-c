from lifelines.utils import concordance_index as ci

def concordance_index(event_times, predicted_scores, event_observed):
    return ci(event_times, -predicted_scores, event_observed)
