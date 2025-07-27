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

@router.get("/me",response_model=list[schemas.ApplicationResponse])
def get_application_by_user_id(current_user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.get_application_by_user_id(current_user=current_user,db=db)

@router.put("/{application_id}",response_model=schemas.ApplicationResponse)
def update_my_application(application_id:int,application:schemas.ApplicationUpdate,current_user:models.User=Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_application(application_id=application_id,application=application,current_user=current_user,db=db)

@router.delete("/{application_id}",status_code=status.HTTP_200_OK)
def delete_application(application_id:int ,db:Session=Depends(get_db),current_user:models.User=Depends(get_current_user)):
    return crud.delete_application(application_id=application_id,current_user=current_user,db=db)
