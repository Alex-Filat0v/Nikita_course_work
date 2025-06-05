from database_module.mongodb import db
from database_module.models import Booking

class BookingService:
    async def create_booking(self, booking: Booking):
        bookings_collection = await db.get_collection("bookings")
        tours_collection = await db.get_collection("tours")

        # Проверяем доступность тура
        tour = await tours_collection.find_one({"id": booking.tour_id})
        if not tour:
            raise Exception("Tour not found")
        if tour["available_slots"] < booking.participants:
            raise Exception("Not enough available slots")

        # Уменьшаем количество доступных мест
        await tours_collection.update_one(
            {"id": booking.tour_id},
            {"$inc": {"available_slots": -booking.participants}}
        )

        # Создаем бронирование
        await bookings_collection.insert_one(booking.dict())
        return {"message": "Booking created successfully"}