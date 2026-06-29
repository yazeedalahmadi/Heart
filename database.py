import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database connection settings. Uses an environment variable when available.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://yazeed:123@localhost:5432/mydb")

# Create the SQLAlchemy engine for database communication.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory so each request can open its own database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models declared in models.py.
Base = declarative_base()

# Dependency used by FastAPI endpoints to get a database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()