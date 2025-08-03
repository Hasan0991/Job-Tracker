from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Инициализируем переменные, но не создаём engine по умолчанию
engine = None
SessionLocal = None
Base = declarative_base()

def init_db(test_engine=None):
    global engine, SessionLocal
    if test_engine:
        engine = test_engine
    else:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is not set in .env file")
        engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
