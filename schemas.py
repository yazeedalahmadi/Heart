from pydantic import BaseModel

# Request schema for the prediction endpoint.
class PatientInput(BaseModel):
    age: int
    anaemia: int
    creatinine_phosphokinase: int
    diabetes: int
    ejection_fraction: int
    high_blood_pressure: int
    platelets: float
    serum_creatinine: float
    serum_sodium: int
    sex: int
    smoking: int
    time: int

# Response schema for patient data returned from the database.
class PatientResponse(PatientInput):
    patient_id: int
    DEATH_EVENT: int

    class Config:
        from_attributes = True

# Response schema for a prediction result.
class PredictionResponse(BaseModel):
    prediction: int