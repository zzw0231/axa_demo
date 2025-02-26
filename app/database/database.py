import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.utils.logger import logger

# Load environment variables from .env
load_dotenv()

# Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.critical("DATABASE_URL is missing or invalid. Check your env.")
    raise ValueError("DATABASE_URL is missing or invalid. Check your env.")
# Create the database engine
try:
    engine = create_engine(DATABASE_URL)
    logger.info("Database connection established successfully.")
except OperationalError as e:
    logger.error(f"Database connection failed: {e}")
    raise e

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the Base class for models
Base = declarative_base()


# Function to create tables automatically
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")


# Dependency to get database session in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise e  # Optional: Re-raise exception for debugging
    finally:
        db.close()
        logger.info("Database session closed.")
