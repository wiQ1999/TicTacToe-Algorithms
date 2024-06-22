from players.abstract_player import AbstractPlayer
from environments.base_game_env import BaseGameEnv
from players.qlearning.qlearning_algorithm import QLearningAlgorithm
from typing import Tuple

class QLearningPlayer(AbstractPlayer):
    def __init__(self, q_table_file='qlearning_table.pkl') -> None:
        self.qlearning = QLearningAlgorithm()
        self.qlearning.load_q_table(q_table_file)

    @property
    def is_clickable(self) -> bool:
        return False

    def auto_move(self, game_state: BaseGameEnv) -> Tuple[int, int]:
        available_moves = game_state.available_moves()
        return self.qlearning.choose_action(game_state, available_moves)

    def update_q_table(self, current_state, action, reward, next_state):
        self.qlearning.update_q_table(current_state, action, reward, next_state)
