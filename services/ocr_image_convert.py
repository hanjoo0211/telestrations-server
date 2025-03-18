import cv2
import numpy as np
import easyocr
import base64
from io import BytesIO
from typing import List
from PIL import Image

# EasyOCR 리더 초기화
OCR_reader = easyocr.Reader(['ko', 'en'])  # 한글과 영어 지원

# resize 크기
RESIZE_FACTOR = 0.1

def preprocess_image(img):
    """ OCR 인식률 향상을 위한 이미지 전처리 """
    # RGBA(4채널) 이미지를 RGB(3채널)로 변환 (투명한 배경을 흰색으로 처리)
    if img.shape[-1] == 4:  
        alpha_channel = img[:, :, 3]  # 알파 채널 분리
        white_background = np.ones_like(img[:, :, :3]) * 255  # 흰색 배경 생성
        alpha_factor = alpha_channel[:, :, np.newaxis] / 255.0  # 알파값 정규화 (0~1)
        img = (img[:, :, :3] * alpha_factor + white_background * (1 - alpha_factor)).astype(np.uint8)  

    # BGR 변환 (필요한 경우)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Grayscale 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 이미지 크기 조정
    resized = cv2.resize(gray, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR, interpolation=cv2.INTER_AREA)

    # 패딩 추가 (테두리에 여백을 추가하여 글자 왜곡 방지)
    padded = cv2.copyMakeBorder(resized, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
    
    # 이진화 처리 (배경과 글자 대비를 높임)
    _, thresh = cv2.threshold(padded, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 전처리된 이미지를 저장
    # cv2.imwrite("preprocessed_image.png", padded)

    return thresh


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
    
    # 이미지 전처리 적용
    processed_img = preprocess_image(img)
    
    # OCR 실행
    result = OCR_reader.readtext(processed_img)
    
    recognized_words = [text for (_bbox, text, _prob) in result]  # 인식된 단어 목록 추출
    return recognized_words


if __name__ == "__main__":
    # ocr_test_images 폴더에 있는 이미지를 Base64로 변환하여 OCR 실행
    import os
    image_directory = "ocr_test_images"
    for image_name in os.listdir(image_directory):
        image_path = os.path.join(image_directory, image_name)
        with open(image_path, "rb") as f:
            base64_str = base64.b64encode(f.read()).decode()
        print(f"File Name: {image_name}, OCR Result: {recognize_text(base64_str)}")
    
    # with open(image_path, "rb") as f:
    #     base64_str = base64.b64encode(f.read()).decode()
    # print(recognize_text(base64_str))
