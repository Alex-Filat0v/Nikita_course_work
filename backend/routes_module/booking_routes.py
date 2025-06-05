from fastapi import APIRouter, HTTPException
from services.booking_service import BookingService
from database_module.models import Booking

booking_router = APIRouter()
booking_service = BookingService()

@booking_router.post("/")
async def create_booking(booking: Booking):
    try:
        return await booking_service.create_booking(booking)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))