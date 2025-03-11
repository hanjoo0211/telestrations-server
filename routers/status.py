from fastapi import APIRouter
from services.game_manager import GameManager

router = APIRouter()
game_manager = GameManager()

@router.get("/status")
async def get_status():
    """현재 게임 상태 반환"""
    return game_manager.get_game_status()
