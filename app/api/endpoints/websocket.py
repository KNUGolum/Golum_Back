from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket import manager

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            # 실시간 처리가 필요하다면 여기에 로직을 추가
            print(f"[WebSocket] User {user_id} sent: {data}")

    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        print(f"[WebSocket] Error with User {user_id}: {e}")
        manager.disconnect(user_id)