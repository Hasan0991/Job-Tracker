from fastapi import APIRouter,HTTPException,status,Depends,Query
from app.database import get_db
from app.schemas import schemas
from app.models import Application
from sqlalchemy.orm import Session
from app import crud
from app.dependencies.auth import get_current_user
from app import models
router=APIRouter(
    prefix="/applications",
    tags=["Applications"]
)
@router.post("/",response_model=schemas.ApplicationResponse,status_code=status.HTTP_201_CREATED)
def apply_to_job(application:schemas.ApplicationCreate,current_user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.create_application(db=db,current_user=current_user,application=application)


@router.get("/",response_model=list[schemas.ApplicationResponse])
def get_all_applications(db:Session=Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)):
    return crud.get_all_applications(db=db,skip=skip,limit=limit)

