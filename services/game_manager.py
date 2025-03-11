class GameManager:
    def __init__(self):
        self.players = []  # 참가자 목록
        self.max_players = 4  # 최대 참가자 수
        self.game_started = False  # 게임 시작 여부
        self.game_round = 0 # 게임 라운드
        self.words = ["임승섭", "채지헌", "최건호", "김한주"]  # 단어 목록
        self.images = [[], [], [], []] # 이미지 목록 (플레이어 순서로 index)


    def add_player(self, websocket):
        """플레이어 추가"""
        if websocket not in self.players and len(self.players) < self.max_players:
            self.players.append(websocket)

        # 4명이 되면 게임 시작
        if len(self.players) == self.max_players:
            self.game_started = True
            self.next_round()
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

    def get_word(self, websocket):
        """플레이어별 단어 반환"""
        if self.game_started and websocket in self.players:
            player_index = self.players.index(websocket)
            word = self.words[player_index]
            return {"word": word}
        return {"word": ""}

    def check_image(self, round):
        """라운드 별로 모든 플레이어가 이미지를 제출했는지 확인"""
        if self.game_round == round:
            for i in range(self.max_players):
                if len(self.images[i]) < round:
                    return False
            return True
        return False

    def next_round(self):
        """라운드 넘기기"""
        self.game_round += 1
        print("Next Round: ", self.game_round)
        return self.game_round
    
    def next_image(self, websocket):
        """다음 이미지 전송"""
        player_index = self.players.index(websocket)
        round = self.game_round
        next_image_index = (player_index + round) % self.max_players
        return {"image": self.images[next_image_index][round - 1]}
