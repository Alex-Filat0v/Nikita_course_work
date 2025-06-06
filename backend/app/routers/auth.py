from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, UserOut
from app.utils.db import db
from app.utils.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing = await db.users.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = hash_password(user.password)
    await db.users.insert_one({"username": user.username, "hashed_password": hashed})
    return {"username": user.username}

@router.post("/login")
async def login(user: UserCreate):
    db_user = await db.users.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}