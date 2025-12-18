# database/engine.py
from sqlmodel import SQLModel, create_engine
from config.settings import settings   # loads DATABASE_URL from .env

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    # Ensure model definitions are imported before running create_all()
    from database import db_models
    SQLModel.metadata.create_all(engine)
