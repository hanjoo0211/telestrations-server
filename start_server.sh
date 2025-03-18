#!/bin/bash

# 가상 환경 활성화
source .venv/bin/activate

# Uvicorn 서버 실행
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --ws-ping-interval 10 --ws-ping-timeout 1200
