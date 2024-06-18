import random
import numpy as np
import pickle
from environments.base_game_env import BaseGameEnv
from environments.player_data import Player

class QLearningAlgorithm:
    def __init__(self, alpha=0.3, gamma=0.99, epsilon=0.9, q_table=None):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = q_table if q_table else {}  # Q-value table

    def get_state_key(self, env: BaseGameEnv) -> str:
        return str(env.board_symbols)

    def choose_action(self, env: BaseGameEnv, available_moves) -> tuple:
        state_key = self.get_state_key(env)
        if state_key not in self.q_table:
            self.q_table[state_key] = {move: 0 for move in available_moves}

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(available_moves)
        else:
            max_value = max(self.q_table[state_key].values())
            best_actions = [move for move, value in self.q_table[state_key].items() if value == max_value]
            return random.choice(best_actions)

    # def update_q_table(self, env: BaseGameEnv, action, reward, next_env: BaseGameEnv):
    #     state_key = self.get_state_key(env)
    #     next_state_key = self.get_state_key(next_env)

    #     if next_state_key not in self.q_table:
    #         self.q_table[next_state_key] = {move: 0 for move in next_env.available_moves()}
        
    #     if state_key not in self.q_table:
    #         self.q_table[state_key] = {action: 0}
    #     elif action not in self.q_table[state_key]:
    #         self.q_table[state_key][action] = 0

    #     old_value = self.q_table[state_key][action]
    #     next_max = max(self.q_table[next_state_key].values(), default=0)

    #     self.q_table[state_key][action] = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        
    def update_q_table(self, env: BaseGameEnv, action, reward, next_env: BaseGameEnv):
        state_key = self.get_state_key(env)
        next_state_key = self.get_state_key(next_env)

        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {move: 0 for move in next_env.available_moves()}

        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0}
        elif action not in self.q_table[state_key]:
            self.q_table[state_key][action] = 0

        old_value = self.q_table[state_key][action]
        next_max = max(self.q_table[next_state_key].values(), default=0)

        # Q-learning update equation
        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[state_key][action] = new_value

        print(f"Updated Q value for state {state_key}, action {action}: {new_value}")

    def load_q_table(self, file_path='qlearning_table.pkl'):
        try:
            with open(file_path, 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print(f"No Q-table file found at {file_path}, starting with an empty Q-table.")

    def choose_action(self, env: BaseGameEnv, available_moves) -> tuple:
        state_key = self.get_state_key(env)
        if state_key not in self.q_table:
            self.q_table[state_key] = {move: 0 for move in available_moves}

        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(available_moves)
            print(f"Choosing random action {action}")
        else:
            max_value = max(self.q_table[state_key].values())
            best_actions = [move for move, value in self.q_table[state_key].items() if value == max_value]
            action = random.choice(best_actions)
            print(f"Choosing best action {action} with Q-value {max_value}")

        return action