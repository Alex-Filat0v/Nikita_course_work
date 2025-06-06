import asyncio
import websockets
import json
import motor.motor_asyncio
import hashlib
from bson import ObjectId

# MongoDB setup
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.travel_db

async def handle_client(websocket):
    print("Client connected")
    try:
        async for message in websocket:
            data = json.loads(message)
            print("Received:", data)

            if data['action'] == 'register':
                # Check if user exists
                existing_user = await db.users.find_one({"username": data['username']})
                if existing_user:
                    response = {"status": "error", "message": "Username already exists"}
                else:
                    # Hash password
                    hashed_pw = hashlib.sha256(data['password'].encode()).hexdigest()
                    user_data = {
                        "username": data['username'],
                        "password": hashed_pw,
                        "email": data.get('email', ''),
                        "full_name": data.get('full_name', '')
                    }
                    # Save to MongoDB
                    result = await db.users.insert_one(user_data)
                    response = {
                        "status": "success",
                        "message": "Registration successful",
                        "user_id": str(result.inserted_id)
                    }
                await websocket.send(json.dumps(response))

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(handle_client, "localhost", 8000):
        print("WebSocket server started at ws://localhost:8000")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())