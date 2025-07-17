from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os 
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()