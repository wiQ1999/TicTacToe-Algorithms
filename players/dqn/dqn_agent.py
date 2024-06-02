import torch
from players.dqn.dq_network import DQNetwork
from players.dqn.replay_buffor import ReplayBuffer
import torch.optim as optim
import torch.nn as nn
import random

class DQNAgent:
    def __init__(self, state_size, action_size, buffer_size=1000, batch_size=32, gamma=0.99, lr=0.001, update_target_every=10):
        self.state_size = state_size
        self.action_size = action_size
        self.batch_size = batch_size
        self.gamma = gamma
        self.update_target_every = update_target_every
        self.buffer = ReplayBuffer(buffer_size)
        self.q_network = DQNetwork(state_size, action_size)
        self.target_network = DQNetwork(state_size, action_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()
        self.steps = 0

    def get_action(self, state, epsilon=0.1):
        if random.random() < epsilon:
            return random.choice(range(self.action_size))
        else:
            state = torch.FloatTensor(state).unsqueeze(0)
            with torch.no_grad():
                q_values = self.q_network(state)
            return q_values.argmax().item()

    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())

    def train_step(self):
        if len(self.buffer) < self.batch_size:
            return

        batch = self.buffer.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)

        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        next_q_values = self.target_network(next_states).max(1)[0]
        target_q_values = rewards + self.gamma * next_q_values * (1 - dones)

        loss = self.loss_fn(current_q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.steps += 1
        if self.steps % self.update_target_every == 0:
            self.update_target_network()
