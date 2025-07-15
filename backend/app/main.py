from fastapi import FastAPI
from .database import engine
from app import models
from app.database import Base

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello fiudshfuiash"}