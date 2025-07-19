from sqlalchemy.orm import Session
from app import models,utils
from app.schemas import schemas
from fastapi import HTTPException,status
from datetime import datetime
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


def get_all_users(db:Session):
    return db.query(models.User).all()

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

def create_job(db:Session,job:schemas.JobCreate):
    new_job=models.Job(
        user_id=job.user_id,
        company_id=job.company_id,
        title=job.title,
        url=job.url,
        status=job.status,
        created_at =datetime.utcnow() ,
        notes=job.notes
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

def get_jobs(db:Session,job_id :int):
    return db.query(models.Job).filter(models.Job.id==job_id).first()

def get_all_jobs(db:Session):
    return db.query(models.Job).all()

