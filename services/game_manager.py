import random
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from .threadpool_ocr import threadpool_ocr


class GameManager:
    def __init__(self):
        self.game_id = None
        self.max_players = 4  # 최대 참가자 수
        self.players = []  # 참가자 목록
        self.ready_status = []  # 참가자 준비 상태
        self.game_started = False  # 게임 시작 여부
        self.game_round = 0 # 게임 라운드
        self.words = ["임승섭", "채지헌", "최건호", "김한주"]  # 단어 목록
        self.result_words = ["임승섭", "채지헌", "최건호", "김한주"]  # 결과 단어 목록
        self.images = [[], [], [], []] # 이미지 목록 (단어 순서로 index)
        self.executor = ThreadPoolExecutor()


    def add_player(self, websocket):
        """플레이어 추가"""
        if websocket not in self.players and len(self.players) < self.max_players:
            self.players.append(websocket)
            self.ready_status.append(False)
        
        print(f"Player Added: {websocket}, Ready: {self.ready_status}")

    def remove_player(self, websocket):
        """플레이어 제거"""
        player_index = self.players.index(websocket)
        self.ready_status.pop(player_index)

        if websocket in self.players:
            self.players.remove(websocket)

        print(f"Player Removed: {websocket}, Ready: {self.ready_status}")

    def get_game_status(self):
        """현재 게임 상태 반환"""
        return {"players": len(self.players), "game_started": self.game_started}

    def start_game(self):
        """게임 시작"""
        if all(self.ready_status) and len(self.players) == self.max_players:
            self.game_started = True
            self.game_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            print(f"Game Started: {self.game_id}")
            return True
        return False
    
    def set_random_word(self):
        """랜덤 단어 설정"""
        with open("resources/words.txt", "r") as f:
            words = f.read().split(",")
        self.words = random.sample(words, self.max_players);
        print(f"Random Words: {self.words}")
        return self.words

    def get_word(self, websocket):
        """플레이어별 단어 반환"""
        if self.game_started and websocket in self.players:
            player_index = self.players.index(websocket)
            word = self.words[player_index]
            return {"word": word}
        return {"word": ""}

    def add_image(self, websocket, data):
        """이미지 저장"""
        if self.game_started:
            player_index = self.players.index(websocket)
            word_index = (player_index + self.game_round - 1) % self.max_players
            self.images[word_index].append(data)

            print(f"Image Added: Player {player_index} Word {word_index} Round {self.game_round}")
            
            # 4라운드 끝나면 OCR 수행하여 결과 업데이트
            if self.game_round == self.max_players:
                self.result_words[word_index] = threadpool_ocr(data, self.executor)
                print(f"Recognized Words: {self.result_words}")
            
            return True
        return False

    def check_image(self, round):
        """라운드 별로 모든 플레이어가 이미지를 제출했는지 확인"""
        if self.game_round == round:
            for i in range(self.max_players):
                if len(self.images[i]) < round:
                    return False
            print(f"All players submitted images for round {round}")
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
        next_image_index = (player_index + self.game_round) % self.max_players
        return {"image": self.images[next_image_index][self.game_round - 1]}

    # 게임 초기화
    def reset_game(self):
        self.game_id = None
        self.players = []
        self.ready_status = []
        self.game_started = False
        self.game_round = 0
        self.words = ["임승섭", "채지헌", "최건호", "김한주"]
        self.result_words = ["임승섭", "채지헌", "최건호", "김한주"]
        self.images = [[], [], [], []]
        self.executor = ThreadPoolExecutor()
        print("Game Reset")
        return True
