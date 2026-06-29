FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Runs the database ingestion script first, then spins up the API server
CMD alembic upgrade head && python load_csv.py && uvicorn main:app --host 0.0.0.0 --port 8000