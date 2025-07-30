from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import models, utils, jwt_handler
from app.schemas import schemas
from app.database import get_db
from app import crud

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = jwt_handler.create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register",
            status_code=status.HTTP_201_CREATED,
            response_model=schemas.UserResponse,
            description="Creates a new user with a hashed password and returns user data without password.")
def register(user:schemas.UserRegister,db:Session=Depends(get_db)):
    return crud.create_user(db=db,user=user,role="user")