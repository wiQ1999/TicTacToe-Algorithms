from environments.base_game_env import BaseGameEnv
from environments.game_state_enum import GameState
from players.abstract_player import AbstractPlayer
from players.human.human_player import HumanPlayer
from players.random.random_player import RandomPlayer
from players.minimax.minimax_player import MiniMaxPlayer
from players.dqn.dqn_player import DQNPlayer
from typing import Dict, List

class UiGameEnv:
    _players_dict: Dict[str, AbstractPlayer] = {
        'Human': HumanPlayer(), 
        'Random': RandomPlayer(),
        'MiniMax': MiniMaxPlayer(),
        'DQN': DQNPlayer()
    }

    def __init__(self):
        self._game = BaseGameEnv()
        self._player_x = self.available_players[0]
        self._player_o = self.available_players[2]
        
    @property
    def player_x(self) -> str:
        return self._player_x
    
    @player_x.setter
    def player_x(self, value):
        self._player_x = value
        self._game.restart()

    @property
    def player_o(self) -> str:
        return self._player_o
    
    @player_o.setter
    def player_o(self, value: str):
        self._player_o = value
        self._game.restart()

    @property
    def available_players(self):
        return list(self._players_dict.keys())
    
    @property
    def state(self) -> str:
        return self._game.game_state.name
    
    @property
    def board_symbols(self) -> List[List[str]]:
        return self._game.board_symbols

    @property
    def board_modifiability(self) -> bool:
        return self._game.game_state == GameState.PLAYING and self._get_current_player().is_clickable
        
    def _get_current_player(self):
        if self._game.current_player.is_x:
            return self._players_dict[self._player_x]
        else:
            return self._players_dict[self._player_o]
        
    def manual_move(self, x: int, y: int) -> bool:
        if self._game.is_position_taken(x, y):
            return False
        self._game.move(x, y)
        return True

    def consider_auto_move(self) -> bool:
        if self._game.game_state != GameState.PLAYING or self._get_current_player().is_clickable:
            return False
        position = None
        if self._game.current_player.is_x:
            position = self._players_dict[self._player_x].auto_move(self._game)
        else:
            position = self._players_dict[self._player_o].auto_move(self._game)
        self._game.move(position[0], position[1])
        return True

    def restart(self):
        self._game.restart()