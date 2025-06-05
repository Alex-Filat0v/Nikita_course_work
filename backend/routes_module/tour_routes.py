from fastapi import APIRouter, HTTPException
from services.tour_service import TourService
from database_module.models import Tour

tour_router = APIRouter()
tour_service = TourService()

@tour_router.get("/")
async def get_tours():
    try:
        return await tour_service.get_all_tours()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tour_router.post("/")
async def create_tour(tour: Tour):
    try:
        return await tour_service.create_tour(tour)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))