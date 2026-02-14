import pandas as pd

def compute_metrics(df_users, df_meetings, df_aic):

    total_meetings = len(df_meetings)

    # -------------------------
    # Adoption
    # -------------------------
    ai_meetings = df_meetings[
        df_meetings["Meeting summary with AI Companion"] == True
    ]

    adoption_rate = (
        len(ai_meetings) / total_meetings
        if total_meetings > 0 else 0
    )

    # -------------------------
    # Repeat Usage
    # -------------------------
    ai_hosts_counts = (
        ai_meetings
        .groupby("Host email")
        .size()
    )

    total_ai_hosts = len(ai_hosts_counts)

    repeat_hosts = len(ai_hosts_counts[ai_hosts_counts >= 2])

    repeat_usage_rate = (
        repeat_hosts / total_ai_hosts
        if total_ai_hosts > 0 else 0
    )

    # -------------------------
    # Trust Index
    # -------------------------
    df_generated = df_aic[
        df_aic["Event Type"] == "Generated"
    ]

    avg_view = df_generated["View Count"].mean()
    avg_regen = df_generated["Regeneration Count"].mean()

    avg_view = avg_view if not pd.isna(avg_view) else 0
    avg_regen = avg_regen if not pd.isna(avg_regen) else 0

    trust_index = avg_view / (1 + avg_regen)

    # -------------------------
    # Department Variance
    # -------------------------
    dept_stats = (
        df_meetings
        .groupby("Department")
        .agg(
            total_meetings=("ID", "count"),
            ai_meetings=("Meeting summary with AI Companion", "sum")
        )
    )

    dept_stats["adoption_rate"] = (
        dept_stats["ai_meetings"] /
        dept_stats["total_meetings"]
    )

    dept_variance = dept_stats["adoption_rate"].std()

    dept_variance = dept_variance if not pd.isna(dept_variance) else 0

    # -------------------------
    # External vs Internal
    # -------------------------
    external_meetings = df_meetings[
        df_meetings["External Ratio"] > 0.5
    ]

    internal_meetings = df_meetings[
        df_meetings["External Ratio"] < 0.2
    ]

    external_adoption = (
        external_meetings["Meeting summary with AI Companion"].sum()
        / len(external_meetings)
        if len(external_meetings) > 0 else 0
    )

    internal_adoption = (
        internal_meetings["Meeting summary with AI Companion"].sum()
        / len(internal_meetings)
        if len(internal_meetings) > 0 else 0
    )

    return {
        "adoption_rate": adoption_rate,
        "repeat_usage_rate": repeat_usage_rate,
        "trust_index": trust_index,
        "dept_variance": dept_variance,
        "external_adoption": external_adoption,
        "internal_adoption": internal_adoption
    }
