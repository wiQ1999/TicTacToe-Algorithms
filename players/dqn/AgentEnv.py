import numpy as np
from typing import List, Tuple
from environments.base_game_env import BaseGameEnv

class AgentEnv:
    def __init__(self, game: BaseGameEnv):
        self.game = game
        self.reset()

    def reset(self):
        self.game.restart()
        return self.get_state()

    def get_state(self):
        # Convert the game board into a flat array (state representation)
        return np.array(self.game._board).flatten()

    def step(self, action: Tuple[int, int]):
        x, y = action
        self.game.move(x, y)
        state = self.get_state()
        reward = self.get_reward()
        done = self.game.game_state != "PLAYING"
        return state, reward, done

    def get_reward(self):
        if self.game.game_state == "X_WIN":
            return 1 if self.game.current_player == "O" else -1
        elif self.game.game_state == "O_WIN":
            return 1 if self.game.current_player == "X" else -1
        elif self.game.game_state == "DRAW":
            return 0
        else:
            return 0

    def available_actions(self) -> List[Tuple[int, int]]:
        return self.game.available_moves()

    def is_done(self):
        return self.game.game_state != "PLAYING"
