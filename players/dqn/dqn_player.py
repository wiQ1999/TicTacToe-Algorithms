import torch
from environments.base_game_env import BaseGameEnv
from players.abstract_player import AbstractPlayer
from players.dqn.agent_env import AgentEnv
from players.dqn.dqn_agent import DQNAgent
from typing import Tuple

class DQNPlayer(AbstractPlayer):
    def __init__(self) -> None:
        super().__init__()
        self.episodes = 1000
        self.epsilon_start = 1.0
        self.epsilon_end = 0.05
        self.epsilon_decay = 0.996
        self.buffer_size = 1000
        self.batch_size = 128
        self.gamma = 0.99
        self.lr = 0.001
        self.update_target_every = 50
        self.env = AgentEnv()
        self.agent = DQNAgent(self.buffer_size, self.batch_size, self.gamma, self.lr, self.update_target_every)
        self.is_trained = False

    @property
    def is_clickable(self) -> bool:
        return False

    def auto_move(self, game_state: BaseGameEnv) -> Tuple[int, int]:
        if not self.is_trained:
            self.train_network()
            self.is_trained = True
        state = self.env.load(game_state)
        action_idx = self.agent.select_target_action(self.env, state)
        x = action_idx // 3
        y = action_idx % 3
        return (x, y)
    
    def train_network(self):
        epsilon = self.epsilon_start
        for episode in range(self.episodes):
            state = self.env.reset()
            done = False
            while not done:
                action_idx = self.agent.select_train_action(self.env, state, epsilon)
                next_state, reward, done = self.env.step(action_idx)
                self.agent.buffer.add((state, action_idx, reward, next_state, done))
                state = next_state
                self.agent.train_step()
            epsilon = max(epsilon * self.epsilon_decay, self.epsilon_end)
            if (episode + 1) % 100 == 0:
                print(f"Episode {episode + 1}/{self.episodes} - Epsilon: {epsilon:.3f}")
        print("Training finished.")
