from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    last_name: str
    email: EmailStr
    username: str

class UserLogin(BaseModel):
    username: str
    password: str
