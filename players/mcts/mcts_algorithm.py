from environments.base_game_env import BaseGameEnv
from environments.game_state_enum import GameState
from typing import Tuple, Optional
import random
import math
from collections import defaultdict

class MCTSAlgorithm:
    def __init__(self):
        self.nodes = {}
        self.current_player = None

    def _get_node(self, state: BaseGameEnv):
        state_key = self._get_state_key(state)
        if state_key not in self.nodes:
            self.nodes[state_key] = {
                "state": state,
                "move": None,
                "parent": None,
                "children": [],
                "visits": 0,
                "wins": 0,
                "unvisited_moves": state.available_moves()
            }
        return self.nodes[state_key]

    def _get_state_key(self, state: BaseGameEnv):
        return str(state.board_symbols) + str(state.current_player)

    def _tree_policy(self, node):
        while not self._is_finished(node["state"]):
            if node["unvisited_moves"]:
                return self._expand(node)
            else:
                node = self._best_child(node, 1.4)
        return node, node["state"]

    def _expand(self, node):
        move = random.choice(node["unvisited_moves"])
        node["unvisited_moves"].remove(move)
        new_state = node["state"].copy()
        new_state.move(move[0], move[1])
        child_node = self._get_node(new_state)
        child_node["move"] = move
        child_node["parent"] = node
        node["children"].append(child_node)
        return child_node, new_state

    def _best_child(self, node, c_param):
        choices_weights = [
            (child["wins"] / child["visits"]) + c_param * math.sqrt((2 * math.log(node["visits"]) / child["visits"]))
            for child in node["children"]
        ]
        return node["children"][choices_weights.index(max(choices_weights))]

    def _default_policy(self, state: BaseGameEnv):
        while not self._is_finished(state):
            move = random.choice(state.available_moves())
            state.move(move[0], move[1])
        return self._get_reward(state)

    def _backup(self, node, reward):
        while node is not None:
            node["visits"] += 1
            if reward == 1:
                node["wins"] += 1
            reward = -reward
            node = node["parent"]

    def _is_finished(self, state: BaseGameEnv):
        return state.game_state in (GameState.X_WIN, GameState.O_WIN, GameState.DRAW)

    def _get_reward(self, state: BaseGameEnv):
        if state.game_state == GameState.X_WIN:
            return 1 if self.current_player == 'X' else -1
        elif state.game_state == GameState.O_WIN:
            return 1 if self.current_player == 'O' else -1
        return 0

    def best_move(self, env: BaseGameEnv, iteration_counter=5000) -> Optional[Tuple[int, int]]:
        self.current_player = 'X' if env.current_player.is_x else 'O'
        if env.turn_count == 0:
            return random.choice(env.available_moves())
        root_state = env.copy()
        self.nodes = {}
        root = self._get_node(root_state)

        for _ in range(iteration_counter):
            node, state = self._tree_policy(root)
            reward = self._default_policy(state.copy())
            self._backup(node, reward)

        return self._best_child(root, 0)["move"]
