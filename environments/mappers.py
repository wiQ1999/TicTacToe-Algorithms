from environments.player_data import Player
from environments.game_state_enum import GameState

PLAYER_VALUE_TO_CHAR = {
    -1: 'X',
    0: ' ',
    1: 'O'
}

PLAYER_TO_WIN_GAME_STATE = {
    Player.create_x(): GameState.X_WIN,
    Player.create_y(): GameState.Y_WIN
}