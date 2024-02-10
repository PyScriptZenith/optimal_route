import os

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv(".env")


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")


POSTGRES_CONNECTION_PATH = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

engine = create_engine(POSTGRES_CONNECTION_PATH,
                       echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
