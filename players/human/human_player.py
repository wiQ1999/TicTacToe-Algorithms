from players.abstract_player import AbstractPlayer
from environments.base_game_env import BaseGameEnv

class HumanPlayer(AbstractPlayer):
    def __init__(self) -> None:
        self.test = 1

    @property
    def is_clickable(self) -> bool:
        return True
    
    def auto_move(self, _: BaseGameEnv):
        return