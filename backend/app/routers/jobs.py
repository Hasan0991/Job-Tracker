from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app import crud,models
from app.database import get_db
from app.schemas import schemas

router=APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)
@router.post("/",responce_model=schemas.JobResponse,status_code=status.HTTP_201_CREATED)
def create_job(job:schemas.JobCreate,db:Session=Depends(get_db)):
    return crud.create_job(db=db,job=job)