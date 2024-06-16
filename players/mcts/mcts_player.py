from players.abstract_player import AbstractPlayer
from players.mcts.mcts_algorithm import MCTSAlgorithm
from environments.base_game_env import BaseGameEnv
from typing import Tuple

class MCTSPlayer(AbstractPlayer):
    @property
    def is_clickable(self) -> bool:
        return False

    def auto_move(self, game_state: BaseGameEnv) -> Tuple[int, int]:
        mcts = MCTSAlgorithm()
        return mcts.best_move(game_state)