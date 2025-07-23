from fastapi import Depends,APIRouter,HTTPException,status
from app.database import get_db
from app.schemas import schemas
from app import crud
from sqlalchemy.orm import Session

router=APIRouter(prefix="/companies",tags=["Companies"])

@router.post("/",response_model=schemas.CompanyResponse)
def create_company(company:schemas.CompanyCreate,db:Session=Depends(get_db)):
    return crud.create_company(company=company,db=db)