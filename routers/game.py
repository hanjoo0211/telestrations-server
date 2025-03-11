from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.broadcast import broadcast
from services.game_manager import GameManager

router = APIRouter()
game_manager = GameManager()

@router.websocket("/game/ready")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    game_started = game_manager.add_player(websocket)
    
    # 현재 참가자 정보 브로드캐스트
    await broadcast({"players": len(game_manager.players), "game_started": game_started}, game_manager.players)
    
    try:
        while True:
            data = await websocket.receive_json()
            await broadcast(data, game_manager.players)
    except WebSocketDisconnect:
        game_manager.remove_player(websocket)
        await broadcast({"players": len(game_manager.players), "game_started": game_manager.game_started}, game_manager.players)
