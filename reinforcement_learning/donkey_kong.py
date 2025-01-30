import pygame
from ale_py import ALEInterface
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

pygame.init()
screen = pygame.display.set_mode((160, 210))

ale = ALEInterface()
ale.setInt('random_seed', 123)
ale.loadROM('roms/donkey_kong.bin')

legal_actions = ale.getLegalActionSet()

class DQN(nn.Module):
    def __init__(self, input_dim, n_actions):
        super(DQN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, n_actions)
        )

    def forward(self, x):
        return self.fc(x)

def select_action(state, policy_net, epsilon):
    if random.random() < epsilon:
        return random.choice(legal_actions)
    with torch.no_grad():
        state = torch.FloatTensor(state).unsqueeze(0)
        return legal_actions[policy_net(state).argmax(dim=1).item()]

def render():
    pygame.event.pump()
    rgb_array = ale.getScreenRGB()
    surface = pygame.surfarray.make_surface(np.transpose(rgb_array, (1, 0, 2)))
    screen.blit(surface, (0, 0))
    pygame.display.flip()


def train_dqn(num_episodes=1000, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.96):
    input_dim = ale.getScreenRGB().size
    n_actions = len(legal_actions)

    policy_net = DQN(input_dim, n_actions)
    optimizer = optim.Adam(policy_net.parameters(), lr=0.0005)

    for episode in range(num_episodes):
        ale.reset_game()
        state = ale.getScreenRGB().flatten()
        total_reward = 0

        while not ale.game_over():
            render()
            action = select_action(state, policy_net, epsilon)
            reward = ale.act(action)
            total_reward += reward

            next_state = ale.getScreenRGB().flatten()

            target = reward + gamma * policy_net(torch.FloatTensor(next_state)).max().item()
            output = policy_net(torch.FloatTensor(state))[legal_actions.index(action)]
            loss = (output - target) ** 2

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            state = next_state

        epsilon = max(epsilon_min, epsilon * epsilon_decay)
        print(f'Episode {episode + 1}, Total Reward: {total_reward}')

train_dqn()

pygame.quit()
