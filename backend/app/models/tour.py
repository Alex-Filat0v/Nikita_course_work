from pydantic import BaseModel
from typing import Optional

class Tour(BaseModel):
    title: str
    country: str
    description: str
    price: float
    available_dates: list[str]
    available_slots: int