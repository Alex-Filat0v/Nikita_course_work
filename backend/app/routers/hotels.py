from fastapi import APIRouter
from app.models.hotel import Hotel
from app.utils.db import db

router = APIRouter(prefix="/hotels", tags=["hotels"])

@router.post("/")
async def add_hotel(hotel: Hotel):
    await db.hotels.insert_one(hotel.dict())
    return {"message": "Hotel added"}

@router.get("/")
async def get_hotels():
    hotels = await db.hotels.find().to_list(100)
    return hotels