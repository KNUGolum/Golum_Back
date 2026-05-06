from typing import Dict
from fastapi import WebSocket

# PR 피드백 반영 - APScheduler에 의해 호출된 정산 결과를 실시간으로 유저에게 전송하기 위한 웹소켓 매니저입니다.
class ConnectionManager:
    def __init__(self):
        # { user_id: websocket_connection }
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"[WebSocket] User {user_id} connected.")

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"[WebSocket] User {user_id} disconnected.")

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"[WebSocket] Broadcast error to {user_id}: {e}")

manager = ConnectionManager()