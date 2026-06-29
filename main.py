from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import joblib
import json
import models
import schemas
from database import engine, get_db

# Ensure the database tables exist before handling requests.
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI application instance.
app = FastAPI()

# Load the trained machine learning model from disk.
model = joblib.load("model.joblib")

# Define a POST endpoint for making a prediction.
@app.post("/predict")
def predict(request: schemas.PatientInput, db: Session = Depends(get_db)):
    # Convert the incoming request into the feature format expected by the model.
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

    # Run the model and extract the predicted class as an integer.
    prediction = int(model.predict(input_data)[0])

    # Save the prediction request and result to the database.
    db_record = models.PredictionRecord(
        input_data=json.dumps(request.model_dump()),
        prediction_result=str(prediction)
    )

    # Commit the new record and refresh it so the generated ID is available.
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record