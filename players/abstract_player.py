from abc import ABC, abstractmethod
from environments.base_game_env import BaseGameEnv
from environments.player_data import Player
from typing import Tuple

class AbstractPlayer(ABC):
    @property
    @abstractmethod
    def is_clickable(self) -> bool:
        raise NotImplementedError()
    
    def init_player(self, player: Player):
        self._player = player
        return

    @abstractmethod
    def auto_move(self, game: BaseGameEnv) -> Tuple[int, int]:
        raise NotImplementedError()
    
    def after_any_move(self, game: BaseGameEnv):
        return