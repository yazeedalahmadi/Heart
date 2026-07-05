from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import joblib
import json
import models
import schemas
from database import engine, get_db
import os
import boto3

# Ensure the database tables exist before handling requests.
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI application instance.
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