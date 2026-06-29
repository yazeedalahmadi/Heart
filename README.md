# Heart Failure Prediction API

A machine learning-powered FastAPI application for predicting heart failure outcomes based on clinical patient data.

## Overview

This project implements a REST API that uses a trained machine learning model to predict the likelihood of heart failure death events. It includes:

- **FastAPI** backend for RESTful predictions
- **PostgreSQL** database to store clinical records and prediction history
- **SQLAlchemy** ORM for database management
- **Alembic** for database migrations
- **Docker & Docker Compose** for containerized deployment
- **Scikit-learn** trained model for predictions

## Features

- ✅ Real-time heart failure predictions via REST API
- ✅ Persistent storage of patient records and prediction history
- ✅ Database migrations with Alembic
- ✅ Docker support for easy deployment
- ✅ Trained model stored as a serialized joblib file
- ✅ Clinical data ingestion from CSV

## Project Structure

```
├── main.py                              # FastAPI application entry point
├── models.py                            # SQLAlchemy ORM models
├── schemas.py                           # Pydantic request/response schemas
├── database.py                          # Database configuration
├── load_csv.py                          # CSV data loader
├── model.joblib                         # Pre-trained ML model
├── requirements.txt                     # Python dependencies
├── Dockerfile                           # Container image definition
├── docker-compose.yml                   # Multi-container orchestration
├── alembic.ini                          # Alembic configuration
├── alembic/                             # Database migration scripts
│   ├── env.py
│   └── versions/
├── heart_failure_clinical_records_dataset.csv  # Clinical dataset
└── README.md                            # This file
```

## Setup & Installation

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker
- Docker Compose

**Steps:**

1. Clone/navigate to the project directory:
   ```bash
   cd c:\Users\yazee\OneDrive\Desktop\Project1
   ```

2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

3. The API will be available at `http://localhost:8000`

4. Access the interactive API documentation at `http://localhost:8000/docs`

### Option 2: Local Setup

**Prerequisites:**
- Python 3.8+
- PostgreSQL running locally

**Steps:**

1. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   alembic upgrade head
   ```

4. Load clinical data (optional):
   ```bash
   python load_csv.py
   ```

5. Start the API server:
   ```bash
   uvicorn main:app --reload
   ```

6. The API will be available at `http://localhost:8000`

## API Endpoints

### POST /predict

Make a prediction for a patient based on clinical features.

**Request Body:**
```json
{
  "age": 50,
  "anaemia": 0,
  "creatinine_phosphokinase": 500,
  "diabetes": 0,
  "ejection_fraction": 38,
  "high_blood_pressure": 1,
  "platelets": 250000,
  "serum_creatinine": 1.1,
  "serum_sodium": 135,
  "sex": 0,
  "smoking": 0,
  "time": 4
}
```

**Response:**
```json
{
  "id": 1,
  "input_data": "{...}",
  "prediction_result": "1"
}
```

**Status Codes:**
- `200 OK` - Prediction successful
- `422 Unprocessable Entity` - Invalid input data

## Database

### Tables

- **patients**: Stores imported clinical records from the CSV file
- **predictions**: Tracks all predictions made through the API

### Migrations

Database migrations are managed with Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Revert migrations
alembic downgrade -1
```

## Data

The project includes `heart_failure_clinical_records_dataset.csv` with the following clinical features:

- **age**: Age of the patient
- **anaemia**: Binary indicator (0 or 1)
- **creatinine_phosphokinase**: Enzyme level (CPK)
- **diabetes**: Binary indicator (0 or 1)
- **ejection_fraction**: Percentage of blood ejected
- **high_blood_pressure**: Binary indicator (0 or 1)
- **platelets**: Platelets in blood (measured in units)
- **serum_creatinine**: Serum creatinine level
- **serum_sodium**: Serum sodium level
- **sex**: Patient gender (0 or 1)
- **smoking**: Smoking status (0 or 1)
- **time**: Follow-up period (days)
- **DEATH_EVENT**: Target variable (0 = survived, 1 = died)

## Dependencies

Key dependencies (see `requirements.txt` for complete list):

- **fastapi** - Modern web framework
- **uvicorn** - ASGI web server
- **sqlalchemy** - SQL toolkit and ORM
- **psycopg2-binary** - PostgreSQL adapter
- **joblib** - Model serialization
- **scikit-learn** - Machine learning library
- **pandas** - Data manipulation
- **alembic** - Database migration tool

## Environment Variables

Create a `.env` file if using local setup (default values work with Docker Compose):

```
DATABASE_URL=postgresql://user:password@localhost/heartfailure_db
```

### Code Structure

- **main.py**: FastAPI application and endpoint definitions
- **models.py**: SQLAlchemy ORM models for database tables
- **schemas.py**: Pydantic models for request/response validation
- **database.py**: Database connection and session management
- **load_csv.py**: Utility to populate database from CSV

## Troubleshooting

### Connection Issues
- Ensure PostgreSQL is running
- Verify DATABASE_URL is correct
- Check database credentials

### Model Loading Issues
- Verify `model.joblib` exists in the project root
- Ensure scikit-learn version matches the one used to train the model

### Docker Issues
- Rebuild containers: `docker-compose down && docker-compose up --build`
- Check logs: `docker-compose logs -f`
