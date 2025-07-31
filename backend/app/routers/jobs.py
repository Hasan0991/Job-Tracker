from fastapi import APIRouter,Depends,status,HTTPException,Query
from sqlalchemy.orm import Session
from app import crud,models
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas import schemas
from app.models import User,Job

router=APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)
@router.post("/",response_model=schemas.JobResponse,status_code=status.HTTP_201_CREATED)
def create_job(job:schemas.JobCreate,current_user: User = Depends(get_current_user),db:Session=Depends(get_db)):
    db_job= db.query(models.Job).filter(Job.title==job.title,Job.user_id==current_user.id).first()
    db_company=db.query(models.Company).filter(models.Company.id==job.company_id).first()
    if job.company_id is not None and not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such company")
    if  db_job:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You can not create same post")
    return crud.create_job(db=db,job=job,current_user_id = current_user.id)

@router.get("/{job_id}",response_model=schemas.JobResponse)
def get_job_by_id(job_id:int ,db:Session=Depends(get_db)):
    job=crud.get_jobs(db=db,job_id=job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Job not found")
    return job

@router.get("/",response_model=list[schemas.JobResponse],status_code=status.HTTP_200_OK)
def get_all_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db:Session=Depends(get_db)
    ):
    return crud.get_jobs_paginated(db,skip=skip,limit=limit)

@router.put("/{job_id}",response_model=schemas.JobResponse)
def update_job(job_id :int,job:schemas.JobUpdate,current_user: User = Depends(get_current_user),db:Session=Depends(get_db)):
    updated_job=crud.update_job_by_id(db=db,job_id=job_id,updated_job=job,current_user_id=current_user.id)
    if not updated_job:
        raise HTTPException(status_code=404,detail="Job not found")
    return updated_job

@router.delete("/{job_id}",status_code=status.HTTP_200_OK)
def delete_job(job_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return crud.delete_job(job_id=job_id,db=db,current_user_id = current_user.id)