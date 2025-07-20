from fastapi import APIRouter,Depends,status,HTTPException,Query
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



@router.get("/",response_model=list[schemas.UserResponse],status_code=status.HTTP_200_OK)
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db:Session=Depends(get_db)
    ):
    return crud.get_all_users(db=db,skip=skip,limit=limit)


@router.get("/{user_id}",response_model=schemas.UserResponse)
def get_user(user_id:int ,db:Session=Depends(get_db)):
    user = crud.get_user_by_id(user_id,db)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user



@router.put("/{user_id}",response_model=schemas.UserResponse)
def update_user(user_id:int,user: schemas.UserUpdate,db:Session=Depends(get_db)):
    return crud.update_user(user_id,db,user_update=user)

@router.delete("/{user_id}",status_code=status.HTTP_200_OK)
def delete_user(user_id: int,db:Session=Depends(get_db)):
    return crud.delete_user(user_id=user_id,db=db)