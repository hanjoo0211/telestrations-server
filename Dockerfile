FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt update && apt install -y \
    libglib2.0-0 libsm6 libxext6 libxrender1 \
 && pip install easyocr opencv-python-headless pillow pytest pytest-asyncio

CMD ["pytest", "-s"]
