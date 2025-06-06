from fastapi import APIRouter, HTTPException
from app.models.tour import Tour
from app.utils.db import db

router = APIRouter(prefix="/tours", tags=["tours"])

@router.post("/")
async def add_tour(tour: Tour):
    await db.tours.insert_one(tour.dict())
    return {"message": "Tour added successfully"}

@router.get("/")
async def get_tours():
    tours = await db.tours.find().to_list(100)
    return tours

@router.get("/hot")
async def get_hot_tours():
    tours = await db.tours.find({"is_hot": True}).to_list(100)
    return tours