from fastapi import APIRouter, HTTPException
from services.user_service import UserService
from database_module.models import User

user_router = APIRouter()
user_service = UserService()

@user_router.post("/register")
async def register(user: User):
    try:
        return await user_service.register_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.post("/login")
async def login(username: str, password: str):
    try:
        return await user_service.login_user(username, password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))