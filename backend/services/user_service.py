from database_module.mongodb import db
from database_module.models import User
from utils.auth import hash_password

class UserService:
    async def register_user(self, user: User):
        users_collection = await db.get_collection("users")
        user.password = hash_password(user.password)
        await users_collection.insert_one(user.dict())
        return {"message": "User registered successfully"}

    async def login_user(self, username: str, password: str):
        users_collection = await db.get_collection("users")
        user = await users_collection.find_one({"username": username})
        if not user:
            raise Exception("User not found")
        if not verify_password(password, user["password"]):
            raise Exception("Invalid password")
        return {"message": "Login successful"}