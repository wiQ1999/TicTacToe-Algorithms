import copy as Copy
from environments.player_data import Player
from environments.game_state_enum import GameState
from environments.mappers import PLAYER_VALUE_TO_CHAR, PLAYER_TO_WIN_GAME_STATE
from typing import List

class BaseGameEnv:
    def __init__(self, board = None):
        if board == None:
            self._board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        else:
            self._board = board
        self._moves_count = 0
        self._player = Player.create_x()
        self._game_state = GameState.PLAYING
    
    @property
    def current_player(self):
        return self._player

    @property
    def game_state(self):
        return self._game_state
    
    @property
    def board_symbols(self) -> List[List[str]]:
        symbols = []
        for x in range(3):
            temp = []
            for y in range(3):
                position = self._board[x][y]
                if position == -1:
                    temp.append(Player.player_x_symbol)
                elif position == 0:
                    temp.append(' ')
                else:
                    temp.append(Player.player_o_symbol)
            symbols.append(temp)
        return symbols
    
    def _check_state(self):
        c1 = self._board[0][0] + self._board[0][1] + self._board[0][2]
        if abs(c1) == 3:
            self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
            return
        c2 = self._board[1][0] + self._board[1][1] + self._board[1][2]
        if abs(c2) == 3:
            self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
            return
        c3 = self._board[2][0] + self._board[2][1] + self._board[2][2]
        if abs(c3) == 3:
            self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
            return
        r1 = self._board[0][0] + self._board[1][0] + self._board[2][0]
        if abs(r1) == 3:
            self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
            return
        r2 = self._board[0][1] + self._board[1][1] + self._board[2][1]
        if abs(r2) == 3:
            self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
            return
        r3 = self._board[0][2] + self._board[1][2] + self._board[2][2]
        if abs(r3) == 3:
            self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
            return
        b1 = self._board[0][0] + self._board[1][1] + self._board[2][2]
        if abs(b1) == 3:
            self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
            return
        b2 = self._board[0][2] + self._board[1][1] + self._board[2][0]
        if abs(b2) == 3:
            self._game_state = PLAYER_TO_WIN_GAME_STATE[self._player]
            return
        if self._moves_count > 8:
            self._game_state = GameState.DRAW
    
    def is_position_taken(self, x: int, y: int):
        return self._board[x][y] != 0
        
    def move(self, x: int, y: int):
        if self._game_state != GameState.PLAYING:
            raise Exception(f'The game is finished.')
        if self.is_position_taken(x, y):
            raise Exception(f'Position ({x},{y}) is already taken.')
        self._board[x][y] = self._player.value
        self._moves_count += 1
        self._check_state()
        self._player = self._player.switch_player()
    
    def available_moves(self):
        moves = []
        for x in range(3):
            for y in range(3):
                position = self._board[x][y]
                if position == 0:
                    moves.append((x, y))
        return moves
    
    def restart(self):
        self._board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self._moves_count = 0
        self._player = Player.create_x()
        self._game_state = GameState.PLAYING

    def copy(self):
        return Copy.deepcopy(self)
    
    def print(self):
        x_len = len(self._board)
        for x_index in range(x_len - 1):
            print('|'.join([PLAYER_VALUE_TO_CHAR[y] for y in self._board[x_index]]))
            print('-+-+-')
        print('|'.join([PLAYER_VALUE_TO_CHAR[y] for y in self._board[x_len - 1]]))