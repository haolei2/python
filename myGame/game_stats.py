class GameStatus():
    def __init__(self,ai_setting):
        self.ai_setting = ai_setting
        self.reset_stats()
        self.game_active = False
        self.score = 0
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        self.ships_left = self.ai_setting.ship_limit
        self.score = 0
        self.level = 1
