from fastapi import APIRouter
from app.utils.db import db

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("/")
async def get_logs():
    logs = await db.logs.find().to_list(100)
    return logs