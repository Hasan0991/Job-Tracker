from fastapi import Depends,APIRouter,HTTPException,status,Query
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas import schemas
from app import crud
from sqlalchemy.orm import Session
from app.models import User
router=APIRouter(prefix="/companies",tags=["Companies"])

@router.post("/",response_model=schemas.CompanyResponse)
def create_company(company:schemas.CompanyCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return crud.create_company(company=company,db=db,current_user_id=current_user.id)

@router.get("/",response_model=list[schemas.CompanyResponse])
def get_all_companies(
    db:Session=Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
    ):
    return crud.get_all_companies(db=db,skip=skip,limit=limit)


@router.get("/{company_id}",response_model=schemas.CompanyResponse)
def get_company_by_id(company_id:int,db:Session=Depends(get_db)):
    return crud.get_company_by_id(db=db,company_id=company_id)


@router.put("/{company_id}",response_model=schemas.CompanyResponse)
def update_company(company_id:int,updated_company:schemas.CompanyUpdate,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_company(company_id=company_id,updated_company=updated_company,db=db,current_user=current_user)

@router.delete("/{company_id}",status_code=status.HTTP_200_OK)
def delete_company(company_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return crud.delete_company(company_id=company_id,db=db,current_user=current_user)