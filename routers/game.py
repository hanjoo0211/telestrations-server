from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.broadcast import broadcast
from services.game_manager import GameManager
from services.image_handler import save_image

router = APIRouter()
game_manager = GameManager()

@router.websocket("/game")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    game_manager.add_player(websocket)
    game_started = game_manager.game_started
    
    # 현재 참가자 정보 브로드캐스트
    await broadcast({"players": len(game_manager.players), "ready": game_manager.ready_status, "game_started": game_started}, game_manager.players)
    
    try:
        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_json()

            # 클라이언트가 게임 준비를 보낸 경우
            if data.get("action") == "start":
                player_index = game_manager.players.index(websocket)
                game_manager.ready_status[player_index] = True
                # 모든 플레이어가 준비 완료
                if all(game_manager.ready_status) and len(game_manager.players) == game_manager.max_players: # "4명"이 모두 준비 완료
                    game_manager.start_game()
                    await broadcast({"players": len(game_manager.players), "ready": game_manager.ready_status, "game_started": game_manager.game_started}, game_manager.players)
                    game_manager.set_random_word()
                    for player in game_manager.players:
                        await player.send_json(game_manager.get_word(player))
                    game_manager.next_round()
                else:
                    await broadcast({"players": len(game_manager.players), "ready": game_manager.ready_status, "game_started": game_manager.game_started}, game_manager.players)

            if game_manager.game_started:
                # 이미지 수신
                if data.get("type") == "image":
                    player_index = game_manager.players.index(websocket)
                    game_manager.images[player_index].append(data["data"])

                    # 이미지 저장
                    save_image(data["data"], player_index, game_manager.game_round, game_manager.game_id)
                    
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
                            print(f"Game End: {game_manager.images}")
                            await broadcast({
                                "type": "game_end",
                                "images": game_manager.images,
                                "first_words": game_manager.words,
                                "result_words": game_manager.result_words
                                }, game_manager.players)

            # await broadcast(data, game_manager.players)
            print(f"Server received from {websocket}: {data}")
    except WebSocketDisconnect:
        # 클라이언트 연결 종료 시 플레이어 제거
        game_manager.remove_player(websocket)
        await broadcast({"players": len(game_manager.players), "game_started": game_manager.game_started}, game_manager.players)
