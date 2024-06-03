import numpy as np
from typing import Tuple, Literal, List
from environments.base_game_env import BaseGameEnv
from environments.game_state_enum import GameState

class AgentEnv:
    def __init__(self, game: BaseGameEnv):
        self.game = game

    def reset(self) -> np.ndarray:
        self.game.restart()
        return self.get_state()
    
    def available_actions(self) -> List[Tuple[int, int]]:
        return self.game.available_moves()

    def get_state(self) -> np.ndarray:
        return np.array(self.game._board).flatten()

    def get_reward(self) -> Literal[-1, 0, 1]:
        if self.game.game_state == GameState.X_WIN:
            return 1 if self.game.current_player.is_o else -1
        elif self.game.game_state == GameState.O_WIN:
            return 1 if self.game.current_player.is_x else -1
        else:
            return 0

    def is_done(self):
        return self.game.game_state != GameState.PLAYING
    
    def step(self, action: Tuple[int, int]) -> Tuple[np.ndarray, Literal[-1, 0, 1], bool]:
        x, y = action
        self.game.move(x, y)
        state = self.get_state()
        reward = self.get_reward()
        done = self.is_done()
        return state, reward, done
