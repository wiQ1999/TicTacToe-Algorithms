from environments.base_game_env import BaseGameEnv
from environments.game_state_enum import GameState
from typing import Tuple, Optional
import random

class MiniMaxAlgorithm():   
    def _minimax(self, env: BaseGameEnv, depth: int, alpha: int, beta: int) -> Tuple[int, Optional[Tuple[int, int]]]:
        if env.game_state == GameState.X_WIN:
            return -10 + depth, None
        if env.game_state == GameState.O_WIN:
            return 10 - depth, None
        if env.game_state == GameState.DRAW:
            return 0, None

        best_move = None
        moves = env.available_moves()
        random.shuffle(moves)

        if env.current_player.is_x:
            best_score = float('inf')
            for move in moves:
                new_env = env.copy()
                new_env.move(move[0], move[1])
                score, _ = self._minimax(new_env, depth + 1, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        else:
            best_score = -float('inf')
            for move in moves:
                new_env = env.copy()
                new_env.move(move[0], move[1])
                score, _ = self._minimax(new_env, depth + 1, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        return best_score, best_move

    def best_move(self, env: BaseGameEnv) -> Optional[Tuple[int, int]]:
        if env.turn_count == 0:
            return random.choice(env.available_moves())
        _, move = self._minimax(env, 0, -float('inf',), float('inf'))
        return move
