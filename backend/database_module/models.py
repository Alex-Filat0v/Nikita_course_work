from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None
    birth_date: Optional[str] = None

class Tour(BaseModel):
    id: str
    country: str
    departure_date: str
    duration: int
    available_slots: int
    price: float

class Booking(BaseModel):
    user_id: str
    tour_id: str
    participants: int
    passport_data: list[str]