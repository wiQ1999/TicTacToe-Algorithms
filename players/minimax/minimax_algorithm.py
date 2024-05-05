from environments.base_game_env import BaseGameEnv

class MinimaxAlgorithm():
    def search(self):
        self._search(True, BaseGameEnv())

    def _search(self, is_maximizer, game_state: BaseGameEnv):
        game_copy = game_state.copy()
        moves = game_copy.available_moves()

        #for move in moves:

    
    def reset(self):
        self.tree = []