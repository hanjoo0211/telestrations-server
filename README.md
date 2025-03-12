# telestrations-server

### Requirements
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### client example
```
const socket = new WebSocket("ws://hzzz.site:8000/game");

socket.onopen = () => {
    console.log("✅ WebSocket 연결됨!");
};

socket.onmessage = (event) => {
    console.log("📩 받은 메시지:", event.data);
};

socket.onerror = (error) => {
    console.log("❌ WebSocket 오류:", error);
};

socket.onclose = () => {
    console.log("❌ WebSocket 연결 종료");
};
```

```
socket.close();
```

### 현재까지 구현
1. browser console에 상단 client example 입력 시 게임 접속 / 준비 -> `{"players": int, "game_started": bool}` 반환
2. 4명 접속 시 모든 client에게 `{"word": str}` 반환
3. 모든 client가 `{"type": "image", "data": "base64imagestr"}` 보내면 다음 라운드로 넘어감
4. 다음 라운드로 넘어가면 각 client에게 `{"image": "base64imagestr"}` 반환
5. 4라운드가 종료되면 모든 client에게 `{"type": "game_end", "images": [모든 이미지 array]}` 반환