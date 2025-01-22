from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import DB_URL
from sqlalchemy.ext.declarative import declarative_base
from src.database.models import Base 

# Base = declarative_base()
engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
