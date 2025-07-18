from pydantic import BaseModel,EmailStr
from datetime import date, datetime
from typing import Optional

class UserCreate(BaseModel):
    email:EmailStr
    password: str
    first_name: Optional[str]=None
    last_name:  Optional[str]=None
    birth_date: Optional[date]=None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[date]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None