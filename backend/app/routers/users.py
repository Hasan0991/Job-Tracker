from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app import models,utils,crud
from app.schemas import schemas
from app.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)