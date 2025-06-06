from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, tours, hotels, booking, logs
import uvicorn

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tours.router)
app.include_router(hotels.router)
app.include_router(booking.router)
app.include_router(logs.router)

connections = set()



from app.routers.ws_handlers import handle_ws_action
import json

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                action = message.get("action")
                payload = message.get("data", {})
                response = await handle_ws_action(action, payload, websocket)
                await websocket.send_text(json.dumps(response))
            except Exception as e:
                await websocket.send_text(json.dumps({"status": "error", "message": f"Bad request: {e}"}))
    except WebSocketDisconnect:
        connections.remove(websocket)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
