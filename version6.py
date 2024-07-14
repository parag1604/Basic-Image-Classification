import torch
import torch.nn as nn
import torch.optim as optim

from common.utils import *
from common.train_utils import *


class Net(nn.Module):
    def __init__(self, num_classes: int = 10) -> None:
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 8, 5, padding="same")
        self.conv2 = nn.Conv2d(8, 16, 3, 1, padding="same")
        self.conv3 = nn.Conv2d(16, 32, 3, 1, padding="same")
        self.conv4 = nn.Conv2d(32, 64, 3, 1, padding="same")
        self.fc1 = nn.Linear(256, 32)
        self.fc2 = nn.Linear(32, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = torch.relu(F.max_pool2d(self.conv1(x), 2))  # 16 x 16 x 8
        x = torch.relu(F.max_pool2d(self.conv2(x), 2))  # 8 x 8 x 16
        x = torch.relu(F.max_pool2d(self.conv3(x), 2))  # 4 x 4 x 32
        x = torch.relu(F.max_pool2d(self.conv4(x), 2))  # 2 x 2 x 64
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = torch.log_softmax(self.fc2(x), dim=1)
        return x


def main() -> None:
    # Load the data
    train_loader, test_loader = get_data('cifar10', batch_size=64)

    # Create a model
    model = Net()
    print("Model Parameter Count:", sum(p.numel() for p in model.parameters()))

    # Create an optimizer
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Train the model
    train(model, train_loader, optimizer, epochs=25)

    # Test the model
    test_loss, test_acc = evaluate(model, test_loader)
    print(f"Test Loss: {test_loss:.4f} | Test Acc: {test_acc:.4f}")