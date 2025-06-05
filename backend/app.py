from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes_module.user_routes import user_router
from routes_module.tour_routes import tour_router
from routes_module.booking_routes import booking_router
from utils.websocket import websocket_endpoint
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(user_router, prefix="/api/users")
app.include_router(tour_router, prefix="/api/tours")
app.include_router(booking_router, prefix="/api/bookings")

# WebSocket
app.add_api_websocket_route("/ws", websocket_endpoint)

# Логирование
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
