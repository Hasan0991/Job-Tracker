from sqlalchemy.orm import Session
from typing import Optional,Union
from app import models,utils
from app.schemas import schemas
from fastapi import HTTPException,status
from datetime import datetime
def create_user(db: Session,user:Union[schemas.UserCreate,schemas.UserRegister],role:Optional[str]=None):
    db_user = db.query(models.User).filter(models.User.email==user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")
    hashed_password = utils.hash_password(user.password)

    new_user= models.User(
        email=user.email,
        password=hashed_password,
        role = role if role else user.role,
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


def get_all_users(db:Session,skip,limit):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(user_id: int , db:Session,user_update:schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id ==user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    for key,value in user_update.dict(exclude_unset=True).items():
        setattr(db_user,key,value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(user_id: int ,db:Session,current_user:models.User):
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if current_user.id!=user_id and current_user.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to view this user")
    db.delete(db_user)
    db.commit()
    return {"details":"user deleted"}

def create_job(db:Session,job:schemas.JobCreate,current_user_id:int):
    new_job=models.Job(
        user_id=current_user_id,
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

def get_jobs_paginated(db:Session,skip: int = 0, limit: int = 10):
    return db.query(models.Job).offset(skip).limit(limit).all()

def update_job_by_id(db:Session,job_id:int,updated_job:schemas.JobUpdate,current_user_id:int):
    db_job = db.query(models.Job).filter(models.Job.id==job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Job post not found")
    if db_job.user_id!=current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this job")
    for key,value in updated_job.dict(exclude_unset=True).items():
        setattr(db_job,key,value)
    
    db.commit()
    db.refresh(db_job)
    return db_job

def delete_job(job_id:int,db:Session,current_user_id:int):
    db_job = db.query(models.Job).filter(models.Job.id==job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Job post not found")
    if db_job.user_id!=current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this job")
    db.delete(db_job)    
    db.commit()
    return {"details":"Job deleted"}


def create_company(db:Session,company:schemas.CompanyCreate,current_user_id:int):
    db_company= db.query(models.Company).filter(models.Company.name==company.name).first()
    if db_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Company already exists")
    new_company=models.Company(
        name=company.name,
        website=company.website,
        description=company.description,
        user_id= current_user_id,
        created_at = datetime.utcnow()
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company
    
def get_all_companies(db:Session,skip,limit):
    return db.query(models.Company).offset(skip).limit(limit).all()

def get_company_by_id(db:Session,company_id:int):
    db_company = db.query(models.Company).filter(models.Company.id==company_id).first()
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such a company")
    return db_company

def update_company(company_id: int,updated_company: schemas.CompanyUpdate,db:Session,current_user:models.User):
    db_company = db.query(models.Company).filter(models.Company.id==company_id).first()
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such a company")
    if db_company.user_id != current_user.id and current_user.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authenticated to update this Company")
    for key,value in updated_company.dict(exclude_unset=True).items():
        setattr(db_company,key,value)
    db.commit()
    db.refresh(db_company)
    return db_company

def delete_company(company_id:int,db:Session,current_user:models.User):
    db_company = db.query(models.Company).filter(models.Company.id==company_id).first()
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Company not found")
    if db_company.user_id!=current_user.id and current_user.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authenticated to delete this Company")
    db.delete(db_company)
    db.commit()
    return {"details":"company deleted"}

def create_application(db:Session,current_user:models.User,application:schemas.ApplicationCreate):
    db_application=db.query(models.Application).filter(models.Application.user_id==current_user.id,models.Application.job_id==application.job_id).first()
    db_job = db.query(models.Job).filter(models.Job.id==application.job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Job not found")
    if db_application:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Already applied to this job")
    new_application=models.Application(
        user_id = current_user.id,
        job_id = application.job_id,
        cover_letter=application.cover_letter
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application