import random
import torch
import torch.nn as nn
import torch.optim as optim
from players.dqn.agent_env import AgentEnv
from players.dqn.dq_network import DQNetwork
from players.dqn.replay_buffer import ReplayBuffer

class DQNAgent:
    def __init__(self, buffer_size, batch_size, gamma, lr, update_target_every):
        self.detect_device()
        self.batch_size = batch_size
        self.gamma = gamma
        self.update_target_every = update_target_every
        self.buffer = ReplayBuffer(buffer_size)
        self.train_network = DQNetwork().to(self.device)
        self.target_network = DQNetwork().to(self.device)
        self.optimizer = optim.Adam(self.train_network.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()
        self.steps = 0

    def detect_device(self):
        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

    def select_train_action(self, env: AgentEnv, state: list, epsilon) -> int:
        if random.random() < epsilon:
            available = env.available_actions()
            return random.choice(available)
        else:
            state = torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)
            with torch.no_grad():
                q_values = self.train_network(state)
            return q_values.argmax().item()

    def select_target_action(self, env: AgentEnv, state: list) -> int:
        state = torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)
        with torch.no_grad():
            q_values = self.target_network(state).flatten()
        print(f'target q_values: {q_values}')
        available = env.available_actions()
        _, indices = q_values.sort(descending=True)
        for max_index in indices:
            if max_index in available:
                break
        return max_index

    def update_target_network(self):
        self.target_network.load_state_dict(self.train_network.state_dict())

    def train_step(self):
        if len(self.buffer) < self.batch_size:
            return

        batch = self.buffer.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(states, dtype=torch.float32, device=self.device)
        actions = torch.tensor(actions, dtype=torch.long, device=self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32, device=self.device)
        next_states = torch.tensor(next_states, dtype=torch.float32, device=self.device)
        dones = torch.tensor(dones, dtype=torch.float32, device=self.device)

        current_q_values = self.train_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        next_q_values = self.target_network(next_states).max(1)[0]
        target_q_values = rewards + self.gamma * next_q_values * (1 - dones)

        loss = self.loss_fn(current_q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.steps += 1
        if self.steps % self.update_target_every == 0:
            self.update_target_network()
