from pydantic import BaseModel,EmailStr
from datetime import date, datetime
from typing import Optional,Literal

class UserCreate(BaseModel):
    email:EmailStr
    password: str
    role: Literal["user", "admin"] = "user"  
    first_name: Optional[str]=None
    last_name:  Optional[str]=None
    birth_date: Optional[date]=None

class UserRegister(BaseModel):
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

class JobCreate(BaseModel):
    company_id: Optional[int]=None
    title: str
    url :str
    status:Optional[str]="sent"
    notes:Optional[str]=None

class JobResponse(BaseModel):
    id: int
    user_id :int
    company_id: Optional[int]
    title:  str
    url : str
    status:Optional[str]
    notes:Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class JobUpdate(BaseModel):
    company_id: Optional[int]=None
    title:Optional[str]=None
    url:Optional[str]=None
    status:Optional[str]=None
    notes:Optional[str]=None

class CompanyCreate(BaseModel):
    name : str
    description: Optional[str]
    website: Optional[str]

class CompanyResponse(BaseModel):
    id: int
    name : Optional[str]
    description: Optional[str]
    website: Optional[str]
    created_at: Optional[datetime]
    class Config:
        from_attributes= True
class CompanyUpdate(BaseModel):
    name: Optional[str]=None
    description: Optional[str]=None
    website: Optional[str]=None

class ApplicationCreate(BaseModel):
    job_id :int
    cover_letter:Optional[str]=None 

class ApplicationUpdate(BaseModel):
    cover_letter:Optional[str]=None
    status: Optional[Literal["pending","accepted","rejected"]] = None

class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    cover_letter: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes= True