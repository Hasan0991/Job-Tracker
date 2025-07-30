from fastapi import APIRouter,Depends,status,HTTPException,Query
from sqlalchemy.orm import Session
from app import models,utils,crud
from app.schemas import schemas
from app.database import get_db
from app.dependencies.auth import get_current_user 
from app.models import User
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    if current_user.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to create this user")
    return crud.create_user(db=db, user=user)



@router.get("/",response_model=list[schemas.UserResponse],status_code=status.HTTP_200_OK)
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db:Session=Depends(get_db)
    ):
    return crud.get_all_users(db=db,skip=skip,limit=limit)

@router.get("/users/me", response_model=schemas.UserResponse)
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    return current_user



@router.get("/{user_id}",response_model=schemas.UserResponse)
def get_user(user_id:int ,current_user: User = Depends(get_current_user),db:Session=Depends(get_db)):
    user = crud.get_user_by_id(user_id,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if user_id!=current_user.id and current_user.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to view this user")
    return user



@router.put("/{user_id}",response_model=schemas.UserResponse)
def update_user(user_id:int,user: schemas.UserUpdate,db:Session=Depends(get_db)):
    return crud.update_user(user_id,db,user_update=user)

@router.delete("/{user_id}",status_code=status.HTTP_200_OK)
def delete_user(user_id: int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return crud.delete_user(user_id=user_id,db=db,current_user=current_user)
