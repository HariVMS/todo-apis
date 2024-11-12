from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.todo import Base

# Database URL (change this to your actual database URL)
DATABASE_URL = "sqlite:///./test.db"  # Use your actual DB connection string

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the database (if not already created)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
