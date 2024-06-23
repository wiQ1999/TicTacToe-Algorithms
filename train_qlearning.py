import pickle
from environments.base_game_env import BaseGameEnv
from players.qlearning.qlearning_algorithm import QLearningAlgorithm
from environments.game_state_enum import GameState

def train_qlearning(num_episodes=10000, alpha=0.3, gamma=0.9, epsilon=0.9):
    qlearning = QLearningAlgorithm(alpha=alpha, gamma=gamma, epsilon=epsilon)

    for episode in range(num_episodes):
        print(f"episode: {episode}")
        env = BaseGameEnv()
        move_count = 0
        while env.game_state == GameState.PLAYING:
            available_moves = env.available_moves()
            action = qlearning.choose_action(env, available_moves)

            # Sprawdzenie czy wybrana pozycja jest już zajęta
            if action not in available_moves:
                continue

            current_state = env.copy()
            reward, current_state, next_state = env.move(action[0], action[1])

            qlearning.update_q_table(current_state, action, reward, next_state)
            move_count += 1

            # Dodanie komunikatów informacyjnych tylko dla ruchu Q-learning
            print(f"Q-learning episode {episode}, move {move_count}:")
            print(f"Chosen action: {action}")
            print(f"Reward: {reward}")
            print("")

        if episode % 100 == 0:
            print(f'Episode {episode}/{num_episodes} completed. Moves in episode: {move_count}')

    with open('qlearning_table.pkl', 'wb') as f:
        pickle.dump(qlearning.q_table, f)

    print(f'Training completed over {num_episodes} episodes.')

if __name__ == '__main__':
    train_qlearning()
