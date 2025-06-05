from database_module.mongodb import db
from database_module.models import Tour

class TourService:
    async def get_all_tours(self):
        tours_collection = await db.get_collection("tours")
        tours = await tours_collection.find().to_list(None)
        return tours

    async def create_tour(self, tour: Tour):
        tours_collection = await db.get_collection("tours")
        await tours_collection.insert_one(tour.dict())
        return {"message": "Tour created successfully"}