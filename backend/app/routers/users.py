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

@router.get("/{user_id}",response_model=schemas.UserResponse)
def get_user(user_id:int ,db:Session=Depends(get_db)):
    user = crud.get_user_by_id(user_id,db)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.put("/{user_id}",response_model=schemas.UserResponse)
def update_user(user_id:int,db:Session,user: schemas.UserUpdate):
    return crud.update_user(user_id=user_id,db=db,user=user)
