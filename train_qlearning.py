import pickle
from environments.base_game_env import BaseGameEnv
from players.qlearning.qlearning_algorithm import QLearningAlgorithm
from environments.game_state_enum import GameState

def train_qlearning(num_episodes=10000, alpha=0.3, gamma=0.9, epsilon=0.1):
    qlearning = QLearningAlgorithm(alpha=alpha, gamma=gamma, epsilon=epsilon)

    for episode in range(num_episodes):
        env = BaseGameEnv()
        while env.game_state == GameState.PLAYING:
            current_state_key = qlearning.get_state_key(env)
            available_moves = env.available_moves()
            action = qlearning.choose_action(env, available_moves)
            reward, current_state, next_state = env.move(action[0], action[1])
            next_state_key = qlearning.get_state_key(next_state)
            qlearning.update_q_table(current_state, action, reward, next_state)

    with open('qlearning_table.pkl', 'wb') as f:
        pickle.dump(qlearning.q_table, f)

    print(f'Training completed over {num_episodes} episodes.')

if __name__ == '__main__':
    train_qlearning()
