import os
import base64
import time
import pytest
import asyncio
from concurrent.futures import ThreadPoolExecutor

from services.ocr_image_convert import recognize_text
from services.threadpool_ocr import threadpool_ocr, threadpool_ocr_async

TEST_IMAGE_PATH = os.path.join("ocr_test_images")

@pytest.fixture
def base64_image_list():
    image_list = []
    for image_name in os.listdir(TEST_IMAGE_PATH):
        with open(os.path.join(TEST_IMAGE_PATH, image_name), "rb") as f:
            image_list.append(base64.b64encode(f.read()).decode())
    return image_list

@pytest.fixture
# 모델 예열
def warmup_model():
    """모델 예열"""
    # 예열할 이미지 경로
    image_path = os.path.join(TEST_IMAGE_PATH, "기타.png")
    
    with open(image_path, "rb") as f:
        base64_str = base64.b64encode(f.read()).decode()
    
    # 모델 예열
    recognize_text(base64_str)

@pytest.mark.asyncio
async def test_parallel_ocr_speed_async(base64_image_list, warmup_model):
    """비동기 병렬 OCR 처리 속도 측정"""
    num_tasks = 4
    executor = ThreadPoolExecutor(max_workers=4)

    start_time = time.time()

    tasks = [
        threadpool_ocr_async(base64_image_list[i % len(base64_image_list)], executor)
        for i in range(num_tasks)
    ]
    results = await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[비동기 병렬 처리] 총 시간: {elapsed:.2f}초")

    assert isinstance(elapsed, float)
    assert results is not None


def test_serial_ocr_speed(base64_image_list, warmup_model):
    """직렬 방식 OCR 처리 속도 측정"""
    num_tasks = 4

    start_time = time.time()
    for i in range(num_tasks):
        recognize_text(base64_image_list[i % len(base64_image_list)])
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"[직렬 처리] 총 시간: {elapsed:.2f}초")

    assert isinstance(elapsed, float)


def test_parallel_ocr_speed(base64_image_list, warmup_model):
    """병렬 방식 OCR 처리 속도 측정"""
    num_tasks = 4

    executor = ThreadPoolExecutor(max_workers=4)
    start_time = time.time()
    for i in range(num_tasks):
        threadpool_ocr(base64_image_list[i % len(base64_image_list)], executor)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"[병렬 처리] 총 시간: {elapsed:.2f}초")

    assert isinstance(elapsed, float)

def test_compare_serial_parallel_async(base64_image_list, warmup_model):
    """직렬, 병렬, 비동기 병렬 처리 비교"""
    num_tasks = 4

    # 직렬 처리
    start_time = time.time()
    for i in range(num_tasks):
        recognize_text(base64_image_list[i % len(base64_image_list)])
    end_time = time.time()
    serial_elapsed = end_time - start_time

    # 병렬 처리
    executor = ThreadPoolExecutor(max_workers=4)
    start_time = time.time()
    for i in range(num_tasks):
        threadpool_ocr(base64_image_list[i % len(base64_image_list)], executor)
    end_time = time.time()
    parallel_elapsed = end_time - start_time

    # 비동기 병렬 처리
    start_time = time.time()
    loop = asyncio.get_event_loop()
    tasks = [
        threadpool_ocr_async(base64_image_list[i % len(base64_image_list)], executor)
        for i in range(num_tasks)
    ]
    loop.run_until_complete(asyncio.gather(*tasks))
    end_time = time.time()
    async_elapsed = end_time - start_time

    print(f"[직렬 처리] 총 시간: {serial_elapsed:.2f}초")
    print(f"[병렬 처리] 총 시간: {parallel_elapsed:.2f}초")
    print(f"[비동기 병렬 처리] 총 시간: {async_elapsed:.2f}초")

    assert isinstance(serial_elapsed, float)
    assert isinstance(parallel_elapsed, float)
    assert isinstance(async_elapsed, float)

    assert serial_elapsed > async_elapsed
    assert parallel_elapsed > async_elapsed