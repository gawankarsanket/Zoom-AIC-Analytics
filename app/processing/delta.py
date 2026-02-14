def compute_delta(current, previous):

    if not previous:
        current["delta_adoption"] = 0
        current["delta_repeat"] = 0
        current["delta_trust"] = 0
        current["delta_variance"] = 0
        return current

    current["delta_adoption"] = (
        current["adoption_rate"] -
        previous.get("adoption_rate", 0)
    )

    current["delta_repeat"] = (
        current["repeat_usage_rate"] -
        previous.get("repeat_usage_rate", 0)
    )

    current["delta_trust"] = (
        current["trust_index"] -
        previous.get("trust_index", 0)
    )

    current["delta_variance"] = (
        current["dept_variance"] -
        previous.get("dept_variance", 0)
    )

    return current
