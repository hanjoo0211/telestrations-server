from .ocr_image_convert import recognize_text

def threadpool_ocr(image_data, executor):
    """OCR을 스레드에서 실행"""
    future = executor.submit(recognize_text, image_data)
    result = future.result()
    return "".join(result) if result else "인식안됨"

import asyncio

async def threadpool_ocr_async(image_data, executor):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, recognize_text, image_data)
