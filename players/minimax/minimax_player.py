from players.abstract_player import AbstractPlayer
from players.minimax.minimax_algorithm import MiniMaxAlgorithm
from environments.base_game_env import BaseGameEnv
from typing import Tuple

class MiniMaxPlayer(AbstractPlayer):
    @property
    def is_clickable(self) -> bool:
        return False

    def auto_move(self, game_state: BaseGameEnv) -> Tuple[int, int]:
        minimax = MiniMaxAlgorithm()
        return minimax.best_move(game_state)