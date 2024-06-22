import pickle
from environments.base_game_env import BaseGameEnv
from players.qlearning.qlearning_algorithm import QLearningAlgorithm
from environments.game_state_enum import GameState

def train_qlearning(num_episodes=10000, alpha=0.3, gamma=0.9, epsilon=0.1):
    qlearning = QLearningAlgorithm(alpha=alpha, gamma=gamma, epsilon=epsilon)

    for episode in range(num_episodes):
        env = BaseGameEnv()
        while env.game_state == GameState.PLAYING:
            available_moves = env.available_moves()
            action = qlearning.choose_action(env, available_moves)
            
            # Sprawdzenie czy wybrana pozycja jest już zajęta
            if action not in available_moves:
                continue
            
            env.move(action[0], action[1])
            reward, current_state, next_state = get_reward(env)
            qlearning.update_q_table(current_state, action, reward, next_state)

    with open('qlearning_table.pkl', 'wb') as f:
        pickle.dump(qlearning.q_table, f)

    print(f'Training completed over {num_episodes} episodes.')

def get_reward(env: BaseGameEnv):
    current_state = env.copy()
    reward = 0
    if env.game_state == GameState.X_WIN:
        reward = 10 if env.current_player.is_x else -10
    elif env.game_state == GameState.O_WIN:
        reward = 10 if not env.current_player.is_x else -10
    elif env.game_state == GameState.DRAW:
        reward = 1
    next_state = env.copy()
    return reward, current_state, next_state

if __name__ == '__main__':
    train_qlearning()
