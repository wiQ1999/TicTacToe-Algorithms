from enum import Enum

class GameState(Enum):
    PLAYING = -2,
    X_WIN = -1,
    DRAW = 0,
    O_WIN = 1