from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.broadcast import broadcast

router = APIRouter()
clients = []  # 현재 연결된 클라이언트 목록

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            await broadcast(data, clients)  # 메시지 브로드캐스트
    except WebSocketDisconnect:
        clients.remove(websocket)
