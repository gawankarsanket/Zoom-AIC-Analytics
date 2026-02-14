def compute_status(metrics):

    # Adoption
    if metrics["delta_adoption"] > 0.03:
        metrics["adoption_status"] = "Improving"
    elif metrics["delta_adoption"] < -0.03:
        metrics["adoption_status"] = "Declining"
    else:
        metrics["adoption_status"] = "Stable"

    # Repeat
    if metrics["delta_repeat"] > 0.03:
        metrics["repeat_status"] = "Improving"
    elif metrics["delta_repeat"] < -0.03:
        metrics["repeat_status"] = "Declining"
    else:
        metrics["repeat_status"] = "Stable"

    # Trust
    if metrics["delta_trust"] > 0.15:
        metrics["trust_status"] = "Improving"
    elif metrics["delta_trust"] < -0.15:
        metrics["trust_status"] = "At Risk"
    else:
        metrics["trust_status"] = "Stable"

    # Variance
    if metrics["delta_variance"] > 0.02:
        metrics["variance_status"] = "Imbalance Increasing"
    elif metrics["delta_variance"] < -0.02:
        metrics["variance_status"] = "Balancing"
    else:
        metrics["variance_status"] = "Stable"

    return metrics
