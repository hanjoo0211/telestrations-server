class GameManager:
    def __init__(self):
        self.players = []  # 참가자 목록
        self.max_players = 4  # 최대 참가자 수
        self.game_started = False  # 게임 시작 여부

    def add_player(self, websocket):
        """플레이어 추가"""
        if websocket not in self.players and len(self.players) < self.max_players:
            self.players.append(websocket)

        # 4명이 되면 게임 시작
        if len(self.players) == self.max_players:
            self.game_started = True
            return True  # 게임이 시작되었음을 반환
        return False  # 아직 시작 전

    def remove_player(self, websocket):
        """플레이어 제거"""
        if websocket in self.players:
            self.players.remove(websocket)

        # 게임 중 참가자가 줄어들면 다시 대기 상태로 변경
        if len(self.players) < self.max_players:
            self.game_started = False

    def get_game_status(self):
        """현재 게임 상태 반환"""
        return {"players": len(self.players), "game_started": self.game_started}
