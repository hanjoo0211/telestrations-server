from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import List

app = FastAPI()

class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'self'; connect-src 'self' ws://hzzz.site:8000 ws://localhost:8000"
        return response

app.add_middleware(CSPMiddleware)

# 현재 연결된 WebSocket 클라이언트 목록
clients: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()  # JSON 데이터 수신
            await broadcast(data)  # 모든 클라이언트에게 전송
    except WebSocketDisconnect:
        clients.remove(websocket)

# 모든 클라이언트에게 메시지 전송
async def broadcast(message: dict):
    for client in clients:
        await client.send_json(message)

# 실행
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
