from fastapi import APIRouter, Depends
from backend.app.dependencies.auth import get_current_user  
from app  import models

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/me")
def read_current_user(user: models.User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email}
