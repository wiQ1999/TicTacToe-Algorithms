import random
import pickle
from environments.base_game_env import BaseGameEnv
from environments.game_state_enum import GameState

class QLearningAlgorithm:
    def __init__(self, alpha=0.3, gamma=0.99, epsilon=0.1, q_table=None):
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
            action = random.choice(available_moves)
        else:
            max_value = max(self.q_table[state_key].values())
            best_actions = [move for move, value in self.q_table[state_key].items() if value == max_value and move in available_moves]
            action = random.choice(best_actions) if best_actions else random.choice(available_moves)

        return action
    
    # def choose_action(self, env: BaseGameEnv, available_moves) -> tuple:
    #     state_key = self.get_state_key(env)
    #     if state_key not in self.q_table:
    #         self.q_table[state_key] = {move: 0 for move in available_moves}

    #     current_player_value = env.current_player.value  # Odczytaj wartość aktualnego gracza (1 dla O, -1 dla X)
    #     if current_player_value == 1:
    #         max_value = max(self.q_table[state_key].values())
    #         best_actions = [move for move, value in self.q_table[state_key].items() if value == max_value and move in available_moves]
    #     else:
    #         min_value = min(self.q_table[state_key].values())
    #         best_actions = [move for move, value in self.q_table[state_key].items() if value == min_value and move in available_moves]

    #     action = random.choice(best_actions) if best_actions else random.choice(available_moves)
    #     return action

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

        # reward = QLearningAlgorithm.get_reward(env)

        # Q-learning update equation
        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[state_key][action] = new_value

        print(f"Updating Q-table for state {state_key}, action {action}:")
        print(f"Old Q-value: {old_value}")
        print(f"Reward: {reward}")
        print(f"Next max Q-value: {next_max}")
        print(f"New Q-value: {new_value}")

    def load_q_table(self, file_path='qlearning_table.pkl'):
        try:
            with open(file_path, 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print(f"No Q-table file found at {file_path}, starting with an empty Q-table.")

    def get_reward(env: BaseGameEnv):
        current_player_value = env.current_player.value
        print(f"QL Player is: {current_player_value}")
        if env.game_state == GameState.X_WIN:
            if current_player_value == 1:
                reward = -1  # Negative reward for O if X wins
            else:
                reward = 1
        elif env.game_state == GameState.O_WIN:
            if current_player_value == 1:
                reward = 1  # Positive reward for O if O wins
            else:
                reward = -1
        elif env.game_state == GameState.DRAW:
            reward = 0  # Neutral reward for draw
        else:
            reward = 0  # No win/loss/draw yet

        return reward
