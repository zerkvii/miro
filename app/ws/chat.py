import json
import uuid
from typing import List, Dict, Any, Union, MutableMapping

from fastapi import Depends
from redis.client import Redis
from starlette.responses import HTMLResponse
from starlette.types import Scope, Receive, Send
from starlette.websockets import WebSocket, WebSocketDisconnect

from app import repository
from app.api.deps import get_current_user, decode_jwt_token
from app.core.config import settings
from app.redis.redis_base import lpush_key, rpush_key, lrange_key
from app.services.logger import get_logger
from app.services.redis import get_redis_conn
from main import app


class WebSocketClient(WebSocket):
    def __init__(self, scope: Scope, receive: Receive, send: Send):
        super().__init__(scope, receive, send)
        self.websocket_id = None
        self.name = None

    def set_uid(self, uid: str):
        self.websocket_id = uid

    def set_name(self, name: str):
        self.name = name

    # async def receive(self) -> Any:
    #     return self.receive()
    # message['name'] = self.name
    # return message


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocketClient] = []

    async def connect(self, webSocketClient: WebSocketClient):
        await webSocketClient.accept()
        self.active_connections.append(webSocketClient)

    def disconnect(self, webSocketClient: WebSocketClient):
        self.active_connections.remove(webSocketClient)

    async def send_personal_message(self, message: Dict[str, Any], webSocketClient):
        await webSocketClient.send_json(message)

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            await connection.send_json(message)

    async def broadcast_exclude(self, uid: str, message: Dict):
        for connection in self.active_connections:
            if connection.websocket_id != uid:
                await connection.send_json(message)

    async def send_history_chat(self, webSocketClient):
        redis_conn = next(get_redis_conn())
        history = lrange_key(redis_conn, settings.CHAT_HISTORY_KEY, '0', '-1')
        print(history)
        chat_history = [json.loads(e) for e in history]
        await webSocketClient.send_json({'msg_type': '30000', 'data': chat_history, 'info': 'get history successful'})


manager = ConnectionManager()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws-apis/chat");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/ws-apis/index")
async def get():
    return HTMLResponse(html)


@app.websocket('/ws-apis/chat')
async def chat(webSocket: WebSocket, con: Redis = Depends(get_redis_conn)):
    logger = next(get_logger())
    webSocketClient = WebSocketClient(webSocket.scope, webSocket.receive, webSocket.send)
    await manager.connect(webSocketClient)
    await manager.send_history_chat(webSocketClient)
    try:
        while True:
            data = await webSocketClient.receive_json()
            print(data['msg_type'])
            if 'msg_type' in data and data['msg_type'] == 20000:
                # webSocketClient.set_name(data['name'])
                if 'x-token' in data:
                    token_data = decode_jwt_token(data['x-token'])
                    current_user = repository.user_repo.get_active_user(con, token_data.sub)
                    if current_user:
                        data['username'] = current_user.username
                        data.pop('x-token')
                        rpush_key(con, settings.CHAT_HISTORY_KEY, [json.dumps(data)])
                        await manager.send_history_chat(webSocketClient)
                    else:
                        logger.error('User not found')

    except WebSocketDisconnect:
        manager.disconnect(webSocketClient)
