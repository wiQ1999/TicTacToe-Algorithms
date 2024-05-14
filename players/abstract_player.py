from abc import ABC, abstractmethod
from environments.base_game_env import BaseGameEnv

class AbstractPlayer(ABC):
    @property
    @abstractmethod
    def is_clickable(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def auto_move(self, game_state: BaseGameEnv):
        raise NotImplementedError()