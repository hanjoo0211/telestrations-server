import base64
import os
from services.game_manager import GameManager

IMAGE_SAVE_FOLDER = "saved_images"
os.makedirs(IMAGE_SAVE_FOLDER, exist_ok=True)

def save_image(base64_string: str, player_index: int, round_number: int, game_id: str) -> str:
    """base64 데이터를 디코딩하여 PNG 파일로 저장"""
    try:
        if not game_id:
            print("❌ Game ID is not set. Cannot save image.")
            return None

        game_folder = os.path.join(IMAGE_SAVE_FOLDER, game_id)
        os.makedirs(game_folder, exist_ok=True)  # 게임별 폴더 생성

        file_name = f"player_{player_index}_round_{round_number}.png"
        file_path = os.path.join(game_folder, file_name)
        
        image_data = base64.b64decode(base64_string)  # base64 디코딩
        with open(file_path, "wb") as file:
            file.write(image_data)
        
        print(f"✅ Image saved: {file_path}")
        return file_path
    except Exception as e:
        print(f"❌ Failed to save image: {e}")
        return None
