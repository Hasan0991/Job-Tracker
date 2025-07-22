from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm  import Session
from app.database import get_db
from app.jwt_handler import decode_access_token
from app import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_user(token: str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW=Authenticate":"Bearer"}
    )
    payload= decode_access_token(token)
    if payload is None or "user_id" not in payload:
        raise credentials_exception
    user=db.query(models.User).filter(models.User.id==payload["user_id"]).first()
    if user is None:
        raise credentials_exception
    return user