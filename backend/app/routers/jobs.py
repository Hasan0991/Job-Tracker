from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app import crud,models
from app.database import get_db
from app.schemas import schemas
from app.models import User
router=APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)
@router.post("/",response_model=schemas.JobResponse,status_code=status.HTTP_201_CREATED)
def create_job(job:schemas.JobCreate,db:Session=Depends(get_db)):
    db_job= db.query(User).filter(User.id==job.user_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such user")
    return crud.create_job(db=db,job=job)

@router.get("/{job_id}",response_model=schemas.JobResponse)
def get_job_by_id(job_id:int ,db:Session=Depends(get_db)):
    job=crud.get_jobs(db=db,job_id=job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Job not found")
    return job

@router.get("/",response_model=list[schemas.JobResponse],status_code=status.HTTP_201_CREATED)
def get_all_jobs(db:Session=Depends(get_db)):
    return crud.get_all_jobs(db)

@router.put("/{job_id}",response_model=schemas.JobResponse)
def update_job(job_id :int,job:schemas.JobUpdate,db:Session=Depends(get_db)):
    updated_job=crud.update_job_by_id(db=db,job_id=job_id,updated_job=job)
    if not updated_job:
        raise HTTPException(status_code=404,detail="Job not found")
    return updated_job

@router.delete("/{job_id}",response_model=status.HTTP_200_OK)
def delete_job(job_id:int,db:Session=Depends(get_db)):
    return crud.delete_job(job_id=job_id,db=db)