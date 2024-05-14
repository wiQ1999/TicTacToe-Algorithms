from players.abstract_player import AbstractPlayer
from environments.base_game_env import BaseGameEnv
from typing import Tuple
import random

class RandomPlayer(AbstractPlayer):
    @property
    def is_clickable(self) -> bool:
        return False

    def auto_move(self, game_state: BaseGameEnv) -> Tuple[int, int]:
        moves = game_state.available_moves()
        return random.choice(moves)