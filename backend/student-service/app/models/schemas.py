from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class StudentRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)

class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None

class StudentResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: Optional[str] = None

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str = "admin"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user: dict
