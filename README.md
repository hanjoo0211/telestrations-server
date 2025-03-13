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
```
socket.send(JSON.stringify({action: "start"}));
```

### 현재까지 구현
1. browser console에 상단 client example 입력 시 게임 접속 / 준비 -> `{"players": int, "ready": List[bool], "game_started": bool}` 반환
2. 각 client가 `{"action": "start"}` 보낼 시 ready 상태 True로 변환 후 `{"players": int, "ready": List[bool], "game_started": bool}` 반환
3. 4명 준비 완료 시 모든 client에게 `{"word": str}` 반환
4. 모든 client가 `{"type": "image", "data": "base64imagestr"}` 보내면 다음 라운드로 넘어감
5. 다음 라운드로 넘어가면 각 client에게 `{"image": "base64imagestr"}` 반환
6. 4라운드가 종료되면 모든 client에게 `{"type": "game_end", "images": [[P1 img 4개], [P2 img 4개], [P3 img 4개], [P4 img 4개]], "first_words": [원래 단어 4개], "result_words": [추론 단어 4개]}` 반환