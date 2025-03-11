from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.broadcast import broadcast
from services.game_manager import GameManager

router = APIRouter()
game_manager = GameManager()

@router.websocket("/game")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    game_started = game_manager.add_player(websocket)
    
    # 현재 참가자 정보 브로드캐스트
    await broadcast({"players": len(game_manager.players), "game_started": game_started}, game_manager.players)

    # 게임 시작 시 모든 플레이어에게 단어 전송
    if game_started:
        for player in game_manager.players:
            await player.send_json(game_manager.get_word(player))
    
    try:
        while True:
            data = await websocket.receive_json()
            await broadcast(data, game_manager.players)
    except WebSocketDisconnect:
        game_manager.remove_player(websocket)
        await broadcast({"players": len(game_manager.players), "game_started": game_manager.game_started}, game_manager.players)
