from fastapi import APIRouter
from app.models.booking import Booking
from app.utils.db import db

router = APIRouter(prefix="/booking", tags=["booking"])

@router.post("/")
async def make_booking(booking: Booking):
    await db.bookings.insert_one(booking.dict())
    await db.logs.insert_one({"event": "booking", "data": booking.dict()})
    return {"message": "Booking created"}