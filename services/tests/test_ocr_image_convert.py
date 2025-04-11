import os
import base64
import time
import pytest
from concurrent.futures import ThreadPoolExecutor

from services.ocr_image_convert import recognize_text
from services.threadpool_ocr import threadpool_ocr

# 테스트에 사용할 이미지 파일 경로
TEST_IMAGE_PATH = os.path.join("ocr_test_images")


@pytest.fixture
def base64_image():
    """OCR 테스트용 Base64 인코딩된 이미지"""
    with open(TEST_IMAGE_PATH + "/기타.png", "rb") as f:
        return base64.b64encode(f.read()).decode()
    
@pytest.fixture
def base64_image_list():
    """OCR 테스트용 Base64 인코딩된 이미지 리스트"""
    image_list = []
    for image_name in os.listdir(TEST_IMAGE_PATH):
        with open(os.path.join(TEST_IMAGE_PATH, image_name), "rb") as f:
            image_list.append(base64.b64encode(f.read()).decode())
    return image_list


def test_serial_ocr_speed(base64_image_list):
    """직렬 방식 OCR 처리 속도 측정"""
    num_tasks = 4  # 실행할 작업 수

    start_time = time.time()
    for i in range(num_tasks):
        recognize_text(base64_image_list[i % len(base64_image_list)])
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"[직렬 처리] 총 시간: {elapsed:.2f}초")

    assert isinstance(elapsed, float)
    assert False


def test_parallel_ocr_speed(base64_image_list):
    """병렬 방식 OCR 처리 속도 측정"""
    num_tasks = 4  # 동시에 실행할 작업 수

    executor = ThreadPoolExecutor(max_workers=4)
    start_time = time.time()
    for i in range(num_tasks):
        threadpool_ocr(base64_image_list[i % len(base64_image_list)], executor)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"[병렬 처리] 총 시간: {elapsed:.2f}초")

    assert isinstance(elapsed, float)
    assert False
