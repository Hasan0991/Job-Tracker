from fastapi import Depends,APIRouter,HTTPException,status,Query
from app.database import get_db
from app.schemas import schemas
from app import crud
from sqlalchemy.orm import Session

router=APIRouter(prefix="/companies",tags=["Companies"])

@router.post("/",response_model=schemas.CompanyResponse)
def create_company(company:schemas.CompanyCreate,db:Session=Depends(get_db)):
    return crud.create_company(company=company,db=db)

@router.get("/",response_model=list[schemas.CompanyResponse])
def get_all_companies(
    db:Session=Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
    ):
    return crud.get_all_companies(db=db,skip=skip,limit=limit)


@router.get("/{company_id}",response_model=list[schemas.CompanyResponse])
def get_company_by_id(company_id:int,db:Session=Depends(get_db)):
    return crud.get_company_by_id(db=db,company_id=company_id)