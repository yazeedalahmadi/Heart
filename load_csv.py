import os
import pandas as pd
from sqlalchemy import create_engine, inspect, text

# Read connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://yazeed:123@localhost:5432/db1")
engine = create_engine(DATABASE_URL)

def ingest_data():
    inspector = inspect(engine)
    
    # Check if the table already exists in PostgreSQL
    if inspector.has_table("patients"):
        # Check if the table already has data inside it
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM patients")).scalar()
            if result > 0:
                print("Database already populated. Skipping data ingestion.")
                return

    print("Ingesting raw dataset into PostgreSQL...")
    df = pd.read_csv("heart_failure_clinical_records_dataset.csv")
    
    # Change 'replace' to 'append' or 'fail' since we handle the check manually
    df.to_sql("patients", engine, if_exists="append", index=True, index_label="patient_id")
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_data()