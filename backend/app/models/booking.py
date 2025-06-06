from pydantic import BaseModel

class Booking(BaseModel):
    username: str
    tour_title: str
    date: str
    participants: int
    passport_data: list[str]