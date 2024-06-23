import copy as Copy
from environments.player_data import Player
from environments.game_state_enum import GameState
from environments.mappers import PLAYER_VALUE_TO_CHAR, PLAYER_TO_WIN_GAME_STATE
from typing import List


class BaseGameEnv:
    def __init__(self, board = None):
        self.restart()
        if board != None:
            self._board = board
    
    @property
    def current_player(self):
        return self._player
    
    @property
    def turn_count(self) -> int:
        return self._turn_count

    @property
    def game_state(self):
        return self._game_state
    
    @property
    def board_symbols(self) -> List[List[str]]:
        return [[PLAYER_VALUE_TO_CHAR[x] for x in y] for y in self._board]
    
    def _check_state(self):
        for y in range(3):
            s = sum(self._board[y][x] for x in range(3))
            if abs(s) == 3:
                self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
                return
            s = sum(self._board[x][y] for x in range(3))
            if abs(s) == 3:
                self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
                return
        s = sum(self._board[i][i] for i in range(3))
        if abs(s) == 3:
            self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
            return
        s = sum(self._board[i][2 - i] for i in range(3))
        if abs(s) == 3:
            self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
            return
        if self._turn_count > 8:
            self._game_state = GameState.DRAW

    def is_position_taken(self, x: int, y: int):
        return self._board[x][y] != 0
        
    def move(self, x: int, y: int):
        if self._game_state != GameState.PLAYING:
            raise Exception(f'The game is finished.')
        if self.is_position_taken(x, y):
            raise Exception(f'Position ({x},{y}) is already taken.')
        current_state = self.copy()  # Stan przed ruchem
        self._board[x][y] = self._player.value
        self._turn_count += 1
        self._check_state()
        reward = self._get_reward()
        next_state = self.copy()  # Stan po ruchu
        self._player = self._player.switch_player()
        return reward, current_state, next_state

    def _get_reward(self):
        if self._game_state == GameState.X_WIN:
            return 1 if self._player.is_x else -1
        if self._game_state == GameState.O_WIN:
            return 1 if self._player.is_o else -1
        if self._game_state == GameState.DRAW:
            return 0.5
        return 0  # Gra w toku

    def available_moves(self):
        moves = []
        for x in range(3):
            for y in range(3):
                if self._board[x][y] == 0:
                    moves.append((x, y))
        return moves
    
    def restart(self):
        self._board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self._turn_count = 0
        self._player = Player.create_x()
        self._game_state = GameState.PLAYING
        return self._board

    def copy(self):
        return Copy.deepcopy(self)
    
    def print(self):
        for y in range(2):
            print('|'.join([PLAYER_VALUE_TO_CHAR[x] for x in self._board[y]]))
            print('-+-+-')
        print('|'.join([PLAYER_VALUE_TO_CHAR[x] for x in self._board[2]]))
