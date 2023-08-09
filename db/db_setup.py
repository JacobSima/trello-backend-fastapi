from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Replace these values with your actual PostgreSQL credentials
POSTGRES_USERNAME = "postgres"
POSTGRES_PASSWORD = "jnjdeploy1"
POSTGRES_HOSTNAME = "192.168.1.101:5434"
POSTGRES_DB_NAME = "opusKanbanDB"
POSTGRES_DB_CONNECT = "postgresql+psycopg2"

load_dotenv(".env")

# Create the connection string
SQLALCHEMY_DATABASE_URL = os.environ["POSTGRES_URL_DOCKER"]
# SQLALCHEMY_DATABASE_URL = os.environ["POSTGRES_URL_LOCAL"]


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}, future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()

# DB Utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()