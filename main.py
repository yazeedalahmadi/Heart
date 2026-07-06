from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from celery.result import AsyncResult
import joblib
import json
import models
import schemas
from database import engine, get_db
import os
import boto3

from tasks import predict_task
from celery_app import celery_app

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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


@app.post("/predict")
def predict(request: schemas.PatientInput, db: Session = Depends(get_db)):
    if not request.patients:
        return {
            "count": 0,
            "results": []
        }
    input_data = [[
        request.age,
        request.anaemia,
        request.creatinine_phosphokinase,
        request.diabetes,
        request.ejection_fraction,
        request.high_blood_pressure,
        request.platelets,
        request.serum_creatinine,
        request.serum_sodium,
        request.sex,
        request.smoking,
        request.time
    ]]

    prediction = int(model.predict(input_data)[0])

    db_record = models.PredictionRecord(
        input_data=json.dumps(request.model_dump()),
        prediction_result=str(prediction)
    )

    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return db_record

@app.post("/predict-batch")
def predict_batch(request: schemas.BatchPatientInput, db: Session = Depends(get_db)):
    input_data = []

    for patient in request.patients:
        input_data.append([
            patient.age,
            patient.anaemia,
            patient.creatinine_phosphokinase,
            patient.diabetes,
            patient.ejection_fraction,
            patient.high_blood_pressure,
            patient.platelets,
            patient.serum_creatinine,
            patient.serum_sodium,
            patient.sex,
            patient.smoking,
            patient.time
        ])

    predictions = model.predict(input_data)

    results = []

    for patient, prediction in zip(request.patients, predictions):
        prediction_int = int(prediction)

        db_record = models.PredictionRecord(
            input_data=json.dumps(patient.model_dump()),
            prediction_result=str(prediction_int)
        )

        db.add(db_record)

        results.append({
            "input": patient.model_dump(),
            "prediction": prediction_int
        })

    db.commit()

    return {
        "count": len(results),
        "results": results
    }


@app.post("/predict-async")
def predict_async(request: schemas.PatientInput):
    input_data = [
        request.age,
        request.anaemia,
        request.creatinine_phosphokinase,
        request.diabetes,
        request.ejection_fraction,
        request.high_blood_pressure,
        request.platelets,
        request.serum_creatinine,
        request.serum_sodium,
        request.sex,
        request.smoking,
        request.time
    ]

    task = predict_task.delay(input_data)

    return {
        "task_id": task.id,
        "status": "queued"
    }


@app.get("/tasks/{task_id}")
def get_task_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None
    }