from sqlalchemy.orm import Session
from app import models,utils
from app.schemas import schemas
from fastapi import HTTPException,status

def create_user(db: Session,user:schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.email==user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")
    hashed_password = utils.hash_password(user.password)

    new_user= models.User(
        email=user.email,
        password=hashed_password,
        first_name = user.first_name,
        last_name = user.last_name,
        birth_date = user.birth_date,

        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(user_id: int,db:Session):
    return db.query(models.User).filter(models.User.id==user_id).first()

def update_user(user_id: int , db:Session,user_update:schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id ==user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    for key,value in user_update.dict(exclude_unset=True).items():
        setattr(db_user,key,value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(user_id: int ,db:Session):
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"details":"user deleted"}