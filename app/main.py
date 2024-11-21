from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import logging

app = FastAPI()

templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.INFO)

@app.get("/", response_class=HTMLResponse)
async def get(request: Request) -> HTMLResponse:
    """
    Ручка стартовой страницы
    """
    return templates.TemplateResponse("index.html", context={"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    Обработка сообщений через websocket сервером
    """
    counter = 0
    await websocket.accept()

    try:
        while True:

            # Получаем данные от клиента
            data = await websocket.receive_text()
            logging.info(f"Получены данные {data}")

            # Парсим полученные данные
            message_data = json.loads(data)
            message = message_data["message"]
            counter += 1

            # Отправляем всем подключенным клиентам сообщение
            response = {'id': counter, 'message': message}
            await websocket.send_text(json.dumps(response))
            logging.info(f"Отправлено: {response}")

    except WebSocketDisconnect:
        # Уведомление об отключении клиента
        logging.info(f"Клиент отключен")
