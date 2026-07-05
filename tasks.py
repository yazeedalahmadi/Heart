import json
import joblib
import os
import boto3
from celery_app import celery_app

MODEL_PATH = "model.joblib"
S3_BUCKET = os.getenv("MODEL_S3_BUCKET")
S3_KEY = os.getenv("MODEL_S3_KEY", "model.joblib")


def download_model_if_needed():
    if os.path.exists(MODEL_PATH):
        return

    if not S3_BUCKET:
        raise RuntimeError("MODEL_S3_BUCKET environment variable is missing")

    s3 = boto3.client("s3")
    s3.download_file(S3_BUCKET, S3_KEY, MODEL_PATH)


download_model_if_needed()
model = joblib.load(MODEL_PATH)


@celery_app.task
def predict_task(input_data):
    prediction = int(model.predict([input_data])[0])
    return prediction