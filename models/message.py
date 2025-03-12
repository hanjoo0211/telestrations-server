from pydantic import BaseModel
from typing import Optional, List

# 기본 메시지 모델
class Message(BaseModel):
    type: str  # 메시지 타입 (예: 'game_update', 'image', 'chat', 등)
    data: dict  # 메시지 내용 (게임 상태, 이미지 데이터 등)

# 게임 상태 업데이트 메시지 모델
class GameStateMessage(BaseModel):
    type: str = "game_update"  # 메시지 타입: 게임 상태 업데이트
    players: int  # 현재 게임 참가자 수
    game_started: bool  # 게임이 시작되었는지 여부

# 이미지 메시지 모델 (Base64 인코딩된 이미지 포함)
class ImageMessage(BaseModel):
    type: str = "image"  # 메시지 타입: 이미지
    data: str  # Base64로 인코딩된 이미지 데이터
