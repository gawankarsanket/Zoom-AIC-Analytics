import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

BASE_DIR = "zoom_synthetic_data"
COMPANY_DOMAIN = "@globalenterprise.com"
EXTERNAL_DOMAIN = "@externalpartner.com"

DEPARTMENTS = [
    "ICTS",
    "Manufacturing",
    "Banking & Finance",
    "Engineering",
    "HR",
    "Operations"
]

# Adoption progression with anomaly (05-06 dip)
ADOPTION_PATTERN = [
    0.50, 0.55, 0.63, 0.70,
    0.68, 0.60,
    0.72, 0.78, 0.82, 0.80, 0.85, 0.88
]

TOTAL_USERS_PATTERN = np.linspace(7000, 9200, 12).astype(int)
LICENSE_PATTERN = np.linspace(1450, 1900, 12).astype(int)

def random_date_within_month(month):
    base = datetime(2024, month, 1)
    day = random.randint(1, 28)
    return base + timedelta(days=day)

def generate_users(total_users, licensed_users, month):
    users = []
    for i in range(total_users):
        dept = random.choice(DEPARTMENTS)
        email = f"user{i}{COMPANY_DOMAIN}"
        join_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 600))
        last_login = random_date_within_month(month)

        license_type = "Licensed" if i < licensed_users else "Basic"

        users.append({
            "Email": email,
            "Employee ID": f"E{i:05}",
            "First Name": f"User{i}",
            "Last Name": "Test",
            "Department": dept,
            "Manager": f"Manager{random.randint(1,100)}",
            "Last Login(UTC)": last_login,
            "Last Client Version": "5.17.10",
            "LicenseType": license_type,
            "LoginType": "SSO",
            "UserStatus": "Active",
            "Location": "Global",
            "Region": "APAC",
            "Join Date": join_date
        })

    return pd.DataFrame(users)

def generate_meetings(users_df, month, adoption_rate):
    meeting_count = random.randint(15000, 20000)
    meetings = []
    aic_logs = []

    licensed_users = users_df[users_df["LicenseType"] == "Licensed"]["Email"].tolist()

    for i in range(meeting_count):
        host = random.choice(users_df["Email"].tolist())
        dept = users_df.loc[users_df["Email"] == host, "Department"].values[0]

        is_external = random.random() < 0.35
        participants = random.randint(2, 15)

        # External ratio simulation
        if is_external:
            external_ratio = round(random.uniform(0.3, 1.0), 2)
        else:
            external_ratio = 0.0





        adoption_probability = adoption_rate

        # Department sensitivity (Engineering + Finance cautious)
        if dept in ["Engineering", "Banking & Finance"]:
            adoption_probability *= 0.85

        # External meetings slightly higher AI usage
        if is_external:
            adoption_probability *= 1.1

        ai_used = random.random() < adoption_probability

        meeting_id = f"M{month:02}{i:06}"
        start_time = random_date_within_month(month)
        duration = random.randint(15, 120)

        meetings.append({
            "Topic": f"Meeting {i}",
            "Type": "Scheduled",
            "ID": meeting_id,
            "Host name": host.split("@")[0],
            "Host email": host,
            "Start time": start_time,
            "End time": start_time + timedelta(minutes=duration),
            "Participants": participants,
            "Duration (minutes)": duration,
            "Total participant minutes": duration * participants,
            "Department": dept,
            "Source": "Zoom",
            "Unique viewers": participants,
            "Max concurrent views": participants,
            "External Ratio": external_ratio,
            "Creation time": start_time - timedelta(minutes=5),
            "Region": "APAC",
            "Screen sharing": random.choice([True, False]),
            "Video on (once in meeting)": True,
            "Remote control": False,
            "Closed caption": ai_used,
            "Breakout room": random.choice([True, False]),
            "Language interpretation": False,
            "Telephone usage with participant ID": False,
            "In-meeting chat": True,
            "Poll": random.choice([True, False]),
            "Join by room": False,
            "Waiting room": True,
            "Live transcription": ai_used,
            "Reaction": True,
            "Zoom App": False,
            "Annotation": False,
            "Raise hand": True,
            "Virtual background": True,
            "Whiteboard": False,
            "Immersive scene": False,
            "Avatar": False,
            "Switch to mobile": False,
            "File sharing": random.choice([True, False]),
            "Meeting summary with AI Companion": ai_used,
            "Meeting questions with AI Companion": ai_used and random.random() < 0.5,
            "Record to computer": False,
            "Record to cloud": random.choice([True, False]),
            "Live translation": False,
            "Registration": False,
            "Smart recording": False,
            "Multi-speaker view": False,
            "Meeting wallpaper (host controlled)": False,
            "GenAI virtual background": False,
            "Multi-share": False,
            "Document collaboration": False,
            "Portrait lighting": False,
            "Personalized audio isolation": False,
            "Color themes": False
        })

        if ai_used:

            # View count grows slightly over months
             
            if month <= 3:
                view_count = random.randint(1, 3)
            else:
                view_count = random.randint(2, 5)

            # Regeneration spike during anomaly (month 5-6)
            if month in [5, 6]:
                regeneration_count = random.randint(1, 3)
            else:
                regeneration_count = random.randint(0, 2)

            aic_logs.append({
            "Meeting ID": meeting_id,
            "Host": host,
            "Feature": "Summary",
            "Event Type": "Generated",
            "Event time": start_time + timedelta(minutes=duration),
            "View Count": view_count,
            "Regeneration Count": regeneration_count
         })

    return pd.DataFrame(meetings), pd.DataFrame(aic_logs)

def generate_all():
    os.makedirs(BASE_DIR, exist_ok=True)

    for month in range(1, 13):
        month_folder = os.path.join(BASE_DIR, f"{month:02}")
        os.makedirs(month_folder, exist_ok=True)

        total_users = TOTAL_USERS_PATTERN[month-1]
        licensed_users = LICENSE_PATTERN[month-1]
        adoption_rate = ADOPTION_PATTERN[month-1]

        users_df = generate_users(total_users, licensed_users, month)
        meetings_df, aic_df = generate_meetings(users_df, month, adoption_rate)

        users_df.to_csv(os.path.join(month_folder, "license_users.csv"), index=False)
        meetings_df.to_csv(os.path.join(month_folder, "meeting_details.csv"), index=False)
        aic_df.to_csv(os.path.join(month_folder, "zoom_aic_feature_log.csv"), index=False)

        print(f"Generated month {month:02}")

if __name__ == "__main__":
    generate_all()
