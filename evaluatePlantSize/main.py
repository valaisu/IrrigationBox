import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from dataloader import dataloader
from architectureUNet import Net


def main():
    net = Net()
    loss_criterion = nn.MSELoss()
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    epochs = 10

    for e in range(epochs):
        running_loss = 0.0
        for images, labels in dataloader():
            optimizer.zero_grad()
            outputs = net(images)
            loss = loss_criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {e}, loss: {running_loss}")

    # Save the model state
    torch.save(net.state_dict(), 'model_state.pth')


if __name__ == '__main__':
    main()

