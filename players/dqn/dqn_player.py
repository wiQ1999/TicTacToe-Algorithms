from environments.base_game_env import BaseGameEnv
from players.dqn.agent_env import AgentEnv
from players.dqn.dqn_agent import DQNAgent

def train_dqn(env, agent, episodes=1000, epsilon_start=1.0, epsilon_end=0.1, epsilon_decay=0.995):
    epsilon = epsilon_start
    for episode in range(episodes):
        state = env.reset()
        done = False
        while not done:
            action_idx = agent.get_action(state, epsilon)
            action = env.available_actions()[action_idx]
            next_state, reward, done = env.step(action)
            agent.buffer.add((state, action_idx, reward, next_state, done))
            state = next_state
            agent.train_step()
        epsilon = max(epsilon * epsilon_decay, epsilon_end)
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}/{episodes} - Epsilon: {epsilon:.3f}")
    print("Training finished.")

# Initialize the environment and agent
game = BaseGameEnv()
env = AgentEnv(game)
state_size = 9  # 3x3 TicTacToe board flattened
action_size = len(env.available_actions())
agent = DQNAgent(state_size, action_size)

# Train the DQN agent
train_dqn(env, agent)

def play_game(env, agent, epsilon=0.0):
    state = env.reset()
    done = False
    while not done:
        if env.game.current_player == "X":
            action_idx = agent.get_action(state, epsilon)
            action = env.available_actions()[action_idx]
        else:
            # Human player or another bot can make a move here
            action = env.available_actions()[0]  # Example: always take the first available move
        state, _, done = env.step(action)
        env.game.print_board()  # Print the board for visualization
    print("Game Over")

# Play a game against the trained agent
play_game(env, agent)
