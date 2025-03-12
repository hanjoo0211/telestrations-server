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
        game_manager.set_random_word()
        for player in game_manager.players:
            await player.send_json(game_manager.get_word(player))
    
    try:
        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_json()

            if game_manager.game_started:
                # 이미지 수신
                if data["type"] == "image":
                    player_index = game_manager.players.index(websocket)
                    game_manager.images[player_index].append(data["data"])
                    
                    # 모든 플레이어가 이미지를 제출했는지 확인
                    if game_manager.check_image(game_manager.game_round):
                        # 각 플레이어들에게 다음 이미지 전송
                        for player in game_manager.players:
                            next_image = game_manager.next_image(player)
                            await player.send_json(next_image)
                        # 라운드 넘기거나 게임 종료
                        if game_manager.game_round < game_manager.max_players:
                            game_manager.next_round()
                        else: # 게임 종료 시 전체 사진 전송
                            await broadcast({"type": "game_end", "images": game_manager.images}, game_manager.players)
                            # game_manager.game_started = False
                            # game_manager.game_round = 0
                            # game_manager.images = [[], [], [], []]

            await broadcast(data, game_manager.players)
    except WebSocketDisconnect:
        # 클라이언트 연결 종료 시 플레이어 제거
        game_manager.remove_player(websocket)
        await broadcast({"players": len(game_manager.players), "game_started": game_manager.game_started}, game_manager.players)
