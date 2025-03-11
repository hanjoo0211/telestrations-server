from fastapi import FastAPI
from routers import game
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

app = FastAPI()

class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'self'; connect-src 'self' ws://hzzz.site:8000 ws://localhost:8000"
        return response

app.add_middleware(CSPMiddleware)

# WebSocket 라우터 등록
app.include_router(game.router)

# 실행
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
