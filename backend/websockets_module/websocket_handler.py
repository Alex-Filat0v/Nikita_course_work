from fastapi import WebSocket
from database_module.database import database
from database_module.models import Message
import json


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    db = database.get_db()

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            print(message_data)

            # Сохраняем сообщение в БД
            message = Message(**message_data)
            await db.messages.insert_one(message.dict())

            # Рассылаем сообщение всем подключенным клиентам
            # В реальном приложении нужно хранить активные соединения
            await websocket.send_text(f"Message received: {message.content}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()