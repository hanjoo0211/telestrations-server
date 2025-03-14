import cv2
import numpy as np
import easyocr
import base64
from io import BytesIO
from typing import List
from PIL import Image

# EasyOCR 리더 초기화
OCR_reader = easyocr.Reader(['ko', 'en'])  # 한글과 영어 지원
# OCR_reader = easyocr.Reader(['ko'])  # 한글만 지원

def recognize_text(base64_str) -> List[str]:
    """ Base64로 인코딩된 이미지 문자열을 OCR로 분석하고 인식된 단어를 반환 """
    # Base64 디코딩
    image_data = base64.b64decode(base64_str)
    
    # 바이너리 데이터를 PIL 이미지로 변환
    image = Image.open(BytesIO(image_data))
    
    # PIL 이미지를 OpenCV 형식(Numpy 배열)으로 변환
    img = np.array(image)
    
    # OpenCV는 BGR 형식으로 처리하므로, RGB -> BGR 변환 (필요할 경우)
    if img.shape[-1] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # OCR 실행
    result = OCR_reader.readtext(img)
    
    recognized_words = [text for (_bbox, text, _prob) in result]  # 인식된 단어 목록 추출
    return recognized_words


if __name__ == "__main__":
    image_path = "test.png"
    with open(image_path, "rb") as f:
        base64_str = base64.b64encode(f.read()).decode()
    print(recognize_text(base64_str))