from players.abstract_player import AbstractPlayer
from environments.base_game_env import BaseGameEnv
import random

class RandomPlayer(AbstractPlayer):
    @property
    def is_clickable(self) -> bool:
        return False

    def auto_move(self, game_state: BaseGameEnv):
        moves = game_state.available_moves()
        next = random.choice(moves)
        game_state.move(next[0], next[1])