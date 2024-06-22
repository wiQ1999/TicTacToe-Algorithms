import torch.nn as nn

class DQNetwork(nn.Module):
    def __init__(self):
        super(DQNetwork, self).__init__()
        self.seq = nn.Sequential(
            nn.Linear(9, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 9)
        )

    def forward(self, x):
        return self.seq(x)
