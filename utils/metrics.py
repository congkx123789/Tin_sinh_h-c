def concordance_index(event_times, predicted_scores, event_observed):
    try:
        from lifelines.utils import concordance_index as ci
    except ImportError:
        print("Warning: lifelines is not installed. Concordance index calculation will fail.")
        return 0.0
    return ci(event_times, -predicted_scores, event_observed)
