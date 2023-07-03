from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

# Replace these values with your actual PostgreSQL credentials
POSTGRES_USERNAME = "postgres"
POSTGRES_PASSWORD = "jnjdeploy1"
POSTGRES_HOSTNAME = "localhost"
POSTGRES_DB_NAME = "opuskanban"
POSTGRES_DB_CONNECT = "postgresql+psycopg2"

encoded_password = urllib.parse.quote(POSTGRES_PASSWORD)

# Create the connection string
SQLALCHEMY_DATABASE_URL = f"{POSTGRES_DB_CONNECT}://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}/{POSTGRES_DB_NAME}"


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