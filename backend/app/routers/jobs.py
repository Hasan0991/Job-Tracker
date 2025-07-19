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