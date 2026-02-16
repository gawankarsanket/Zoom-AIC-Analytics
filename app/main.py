from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
import json

from app.processing.loader import load_data
from app.processing.metrics import compute_metrics
from app.processing.delta import compute_delta
from app.processing.status import compute_status

app = FastAPI(title="Zoom AI Analytics Engine")


@app.post("/process-month")
async def process_month(
    month: str = Form(...),
    license_users: UploadFile = File(...),
    meeting_details: UploadFile = File(...),
    zoom_aic_feature_log: UploadFile = File(...),
    previous_metrics: Optional[str] = Form(None)
):

    # Load CSVs into DataFrames
    df_users, df_meetings, df_aic = load_data(
        license_users,
        meeting_details,
        zoom_aic_feature_log
    )

    # Compute deterministic metrics
    current_metrics = compute_metrics(df_users, df_meetings, df_aic)

    # Parse previous metrics JSON if provided
    prev_metrics_dict = None

    if previous_metrics:
        previous_metrics = previous_metrics.strip()
        if previous_metrics and previous_metrics != "null":
            try:
                prev_metrics_dict = json.loads(previous_metrics)
            
            except json.JSONDecodeError:
                prev_metrics_dict = None
                


    

    # Compute delta
    metrics_with_delta = compute_delta(current_metrics, prev_metrics_dict)

    # Compute status classification
    final_metrics = compute_status(metrics_with_delta)

    return {
        "month": month,
        "metrics": final_metrics
    }
