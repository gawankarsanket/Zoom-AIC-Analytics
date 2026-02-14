import pandas as pd

def load_data(license_file, meeting_file, aic_file):

    df_users = pd.read_csv(license_file.file)
    df_meetings = pd.read_csv(meeting_file.file)
    df_aic = pd.read_csv(aic_file.file)

    # Basic cleaning
    df_meetings["Meeting summary with AI Companion"] = \
        df_meetings["Meeting summary with AI Companion"].astype(bool)

    df_meetings["External Ratio"] = \
        pd.to_numeric(df_meetings["External Ratio"], errors="coerce").fillna(0)

    return df_users, df_meetings, df_aic
