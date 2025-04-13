# telestrations-server

![image](https://github.com/user-attachments/assets/7e538cef-167a-4b87-b6a3-f2fba7ce354e)

![image](https://github.com/user-attachments/assets/bcec934b-fab5-4e19-93fb-91f58d74e28b)
![image](https://github.com/user-attachments/assets/05e9d579-3d37-4c0d-8b77-8efbeca79f09)
![image](https://github.com/user-attachments/assets/c9e625f0-7fc5-40c6-90d2-fe5f3f0e10ef)


### Requirements
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --ws-ping-interval 10 --ws-ping-timeout 1200
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
socket.send(JSON.stringify({"action": "start"}));
```

### 현재까지 구현
1. browser console에 상단 client example 입력 시 게임 접속 / 준비 -> `{"players": int, "ready": List[bool], "game_started": bool}` 반환
2. 각 client가 `{"action": "start"}` 보낼 시 ready 상태 True로 변환 후 `{"players": int, "ready": List[bool], "game_started": bool}` 반환
3. 4명 준비 완료 시 모든 client에게 `{"word": str}` 반환
4. 모든 client가 `{"type": "image", "data": "base64imagestr"}` 보내면 다음 라운드로 넘어감
5. 다음 라운드로 넘어가면 각 client에게 `{"image": "base64imagestr"}` 반환
6. 4라운드가 종료되면 모든 client에게 `{"type": "game_end", "images": [[word1 img 4개], [word2 img 4개], [word3 img 4개], [word4 img 4개]], "first_words": [원래 단어 4개], "result_words": [OCR 추론 단어 4개]}` 반환
