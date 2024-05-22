from environments.base_game_env import BaseGameEnv
from environments.game_state_enum import GameState
from typing import Tuple, Optional

class MiniMaxAlgorithm():   
    def minimax_test(self, env: BaseGameEnv, depth: int) -> Tuple[int, Tuple[int, int] | None]:
        if env.game_state == GameState.X_WIN:
            return -10 + depth, None
        if env.game_state == GameState.O_WIN:
            return 10 - depth, None
        if env.game_state == GameState.DRAW:
            return 0, None

        if env.current_player.is_x:
            best_score = 10
            best_move = None
            for move in env.available_moves():
                new_env = env.copy()
                new_env.move(move[0], move[1])
                score, _ = self.minimax_test(new_env, depth + 1)
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = -10
            best_move = None
            for move in env.available_moves():
                new_env = env.copy()
                new_env.move(move[0], move[1])
                score, _ = self.minimax_test(new_env, depth + 1)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        
    def _minimax(self, env: BaseGameEnv, depth: int, alpha: int, beta: int) -> Tuple[int, Optional[Tuple[int, int]]]:
        if env.game_state == GameState.X_WIN:
            return -10 + depth, None
        if env.game_state == GameState.O_WIN:
            return 10 - depth, None
        if env.game_state == GameState.DRAW:
            return 0, None

        best_move = None

        if env.current_player.is_x:
            best_score = float('inf')
            for move in env.available_moves():
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
            for move in env.available_moves():
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
        _, move = self._minimax(env, 0, -float('inf'), float('inf'))
        return move
