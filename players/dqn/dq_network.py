import torch
import torch.nn as nn

class DQNetwork(nn.Module):
    def __init__(self):
        super(DQNetwork, self).__init__()
        self.flatten = nn.Flatten(0, 1)
        self.seq = nn.Sequential(
            nn.Linear(9, 36),
            nn.ReLU(),
            nn.Linear(36, 36),
            nn.ReLU(),
            nn.Linear(36, 9),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.seq(x)
