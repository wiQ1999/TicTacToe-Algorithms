import torch.nn as nn

class DQNetwork(nn.Module):
    def __init__(self):
        super(DQNetwork, self).__init__()
        self.seq = nn.Sequential(
            nn.Linear(9, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 9)
        )

    def forward(self, x):
        return self.seq(x)
