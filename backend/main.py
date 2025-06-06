import asyncio
import websockets
import json
import motor.motor_asyncio
import hashlib
from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.travel_db

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


async def handle_client(websocket):
    print("Client connected")
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")
            response = {"status": "error", "message": "Unknown action"}

            if action == "register":
                existing = await db.users.find_one({"username": data["username"]})
                if existing:
                    response = {"status": "error", "message": "Username already exists"}
                else:
                    user = {
                        "username": data["username"],
                        "email": data["email"],
                        "password": hash_password(data["password"])
                    }
                    await db.users.insert_one(user)
                    response = {"status": "success", "message": "Registered"}

            elif action == "login":
                user = await db.users.find_one({"email": data["username"]})
                if user and user["password"] == hash_password(data["password"]):
                    response = {"status": "success", "message": "Login successful", "user_id": str(user["_id"])}
                else:
                    response = {"status": "error", "message": "Invalid login or password"}

            elif action == "get_tours":
                tours = await db.tours.find().to_list(length=100)
                for t in tours:
                    t["_id"] = str(t["_id"])
                response = {"status": "success", "tours": tours}

            elif action == "get_hotels":
                hotels = await db.hotels.find().to_list(length=100)
                for h in hotels:
                    h["_id"] = str(h["_id"])
                response = {"status": "success", "hotels": hotels}

            elif action == "get_countries":
                countries = await db.countries.find().to_list(length=100)
                response = {"status": "success", "countries": countries}

            elif action == "book_tour":
                tour_id = data["tour_id"]
                tour = await db.tours.find_one({"_id": ObjectId(tour_id)})
                if not tour or tour.get("available_slots", 0) <= 0:
                    response = {"status": "error", "message": "No available slots"}
                else:
                    booking = {
                        "user_id": data["user_id"],
                        "tour_id": tour_id,
                        "hotel_id": data.get("hotel_id"),
                        "date": data.get("date"),
                        "passport_info": data.get("passport_info"),
                        "people": data.get("people", 1)
                    }
                    await db.bookings.insert_one(booking)
                    await db.tours.update_one({"_id": ObjectId(tour_id)}, {"$inc": {"available_slots": -1}})
                    response = {"status": "success", "message": "Booking confirmed"}

            await websocket.send(json.dumps(response))

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")


async def main():
    async with websockets.serve(handle_client, "localhost", 8000):
        print("WebSocket server started on ws://localhost:8000")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
