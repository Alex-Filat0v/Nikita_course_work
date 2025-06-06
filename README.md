# Backend для сайта турагентства

## Запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите сервер:
```bash
uvicorn main:app --reload
```

3. Убедитесь, что MongoDB работает на `localhost:27017` или настройте `.env`

4. WebSocket доступен по: `ws://localhost:8000/ws`

## Эндпоинты

- `/auth/register`, `/auth/login`
- `/tours/`, `/tours/hot`
- `/hotels/`
- `/booking/`
- `/logs/`