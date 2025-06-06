from pydantic import BaseModel

class Hotel(BaseModel):
    name: str
    country: str
    city: str
    stars: int
    description: str
    available_rooms: int