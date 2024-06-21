import numpy as np
from typing import Tuple, Literal, List
from environments.base_game_env import BaseGameEnv
from environments.game_state_enum import GameState

class AgentEnv:
    def __init__(self):
        self._game = BaseGameEnv()
        self._wrong_move = False
    
    def reset(self) -> np.ndarray:
        self._game.restart()
        self._wrong_move = False
        return self.get_state()
    
    def available_actions(self) -> List[Tuple[int, int]]:
        return self._game.available_moves()

    def get_state(self) -> np.ndarray:
        return np.array(self._game._board).flatten()

    def get_reward(self) -> Literal[-1, 0, 1]:
        if self._wrong_move:
            return -1
        elif self._game.game_state == GameState.X_WIN:
            return 1 if self._game.current_player.is_o else -1
        elif self._game.game_state == GameState.O_WIN:
            return 1 if self._game.current_player.is_x else -1
        else:
            return 0

    def is_done(self):
        return self._wrong_move or self._game.game_state != GameState.PLAYING
    
    def step(self, action: int) -> Tuple[np.ndarray, Literal[-1, 0, 1], bool]:
        x = action // 3
        y = action % 3
        if self._game.is_position_taken(x, y):
            self._wrong_move = True
        else:
            self._game.move(x, y)
        state = self.get_state()
        reward = self.get_reward()
        done = self.is_done()
        return state, reward, done
