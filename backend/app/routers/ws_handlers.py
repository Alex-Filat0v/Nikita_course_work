from app.utils.db import db
from app.utils.security import hash_password, verify_password
from app.models.profile import UserProfile
from app.models.booking import Booking
from app.models.tour import Tour
from app.models.hotel import Hotel
import json

async def handle_ws_action(action, payload, websocket):
    if action == "get_tours":
        tours = await db.tours.find().to_list(100)
        return {"status": "success", "data": tours}

    elif action == "get_hotels":
        hotels = await db.hotels.find().to_list(100)
        return {"status": "success", "data": hotels}

    elif action == "search_tours":
        country = payload.get("country")
        date = payload.get("date")
        tours = await db.tours.find({"country": country, "available_dates": date}).to_list(100)
        return {"status": "success", "data": tours}

    elif action == "book_tour":
        booking = Booking(**payload)
        # Проверка на доступность мест
        tour = await db.tours.find_one({"title": booking.tour_title, "available_dates": booking.date})
        if not tour:
            return {"status": "error", "message": "Tour not found"}
        if tour["available_slots"] < booking.participants:
            return {"status": "error", "message": "Not enough slots"}
        await db.bookings.insert_one(booking.dict())
        await db.tours.update_one(
            {"title": booking.tour_title, "available_dates": booking.date},
            {"$inc": {"available_slots": -booking.participants}}
        )
        return {"status": "success", "message": "Booking confirmed"}

    elif action == "get_profile":
        username = payload.get("username")
        profile = await db.profiles.find_one({"username": username})
        return {"status": "success", "data": profile or {}}

    elif action == "update_profile":
        profile = UserProfile(**payload)
        await db.profiles.update_one(
            {"username": profile.username},
            {"$set": profile.dict()},
            upsert=True
        )
        return {"status": "success", "message": "Profile updated"}

    return {"status": "error", "message": "Unknown action"}

from app.models.user import UserCreate
from app.utils.security import hash_password, verify_password

async def handle_ws_action(action, payload, websocket):
    if action == "register":
        username = payload.get("username")
        password = payload.get("password")
        print(username, password)


        if not username or not password:
            return {"status": "error", "message": "Username and password required"}
        existing = await db.users.find_one({"username": username})
        if existing:
            return {"status": "error", "message": "User already exists"}
        hashed = hash_password(password)
        await db.users.insert_one({"username": username, "hashed_password": hashed})
        return {"status": "success", "message": "Registered successfully"}

    elif action == "login":
        username = payload.get("username")
        password = payload.get("password")
        user = await db.users.find_one({"username": username})
        if not user or not verify_password(password, user["hashed_password"]):
            return {"status": "error", "message": "Invalid credentials"}
        return {"status": "success", "message": "Login successful"}

    elif action == "subscribe":
        email = payload.get("email")
        if email:
            await db.subscribers.insert_one({"email": email})
            return {"status": "success", "message": "Subscribed!"}
        return {"status": "error", "message": "Email required"}