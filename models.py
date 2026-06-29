from sqlalchemy import Column, Integer, Float, String
from database import Base

# Stores each prediction made through the API.
class PredictionRecord(Base):
    # Name of the table used to store prediction history.
    __tablename__ = "predictions"

    # Auto-incrementing primary key for each row.
    id = Column(Integer, primary_key=True, index=True)

    # JSON string of the input features received from the request.
    input_data = Column(String)

    # Prediction returned by the model for that input.
    prediction_result = Column(String)


# Represents the patient data loaded from the CSV file.
class Patient(Base):
    # Name of the table that stores the imported clinical data.
    __tablename__ = "patients"

    # Primary key matching the CSV row index.
    patient_id = Column(Integer, primary_key=True)

    # Clinical features used by the prediction model.
    age = Column(Integer)
    anaemia = Column(Integer)
    creatinine_phosphokinase = Column(Integer)
    diabetes = Column(Integer)
    ejection_fraction = Column(Integer)
    high_blood_pressure = Column(Integer)
    platelets = Column(Float)
    serum_creatinine = Column(Float)
    serum_sodium = Column(Integer)
    sex = Column(Integer)
    smoking = Column(Integer)
    time = Column(Integer)

    # Target label indicating whether the patient died.
    DEATH_EVENT = Column(Integer)