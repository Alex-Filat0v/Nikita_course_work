from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    username: str
    email: EmailStr
    password_hash: str


class Tour(BaseModel):
    title: str
    description: str
    price: float
    duration: int
    is_active: bool = True
    created_at: datetime = datetime.now()
