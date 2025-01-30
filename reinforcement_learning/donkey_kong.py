"""
Deep Q-Learning for Donkey Kong with Pygame and ALE  
Author: Maksymilian Mrówka, Maciej Uzarski  

Environment Setup:  
1. Navigate to the directory containing the script:  
   - `cd path/to/deep_q_learning`  
2. Install required dependencies:  
   - `pip install -r requirements.txt`  
3. Run the script:  
   - Execute the script with `python donkey_kong.py`  

Description:  
- This script implements a deep Q-learning agent that plays the classic arcade game Donkey Kong using the Arcade Learning Environment (ALE) and Pygame.  
- The agent learns optimal actions by interacting with the game environment and updating its policy through neural network-based Q-value approximation.  
- The training process uses epsilon-greedy action selection and backpropagation to update the network weights.  

Features:  
1. **Deep Q-Network Architecture**:  
   - The network consists of a fully connected architecture that takes game state inputs and outputs Q-values for possible actions.  
2. **Epsilon-Greedy Action Selection**:  
   - The agent balances exploration and exploitation by selecting random actions with a probability controlled by an epsilon parameter, which decays over time.  
3. **Real-Time Game Rendering**:  
   - Pygame is used to render the current game state in real time, displaying the gameplay progress as the agent learns.  
4. **Game Interaction via ALE**:  
   - The Arcade Learning Environment provides an interface to control Donkey Kong and gather feedback on actions and rewards.  
5. **Learning Through Temporal-Difference Updates**:  
   - The agent updates its Q-values using temporal-difference learning, with the Bellman equation guiding updates based on rewards and future state estimates.  

Output:  
- The script logs the total reward obtained by the agent at the end of each training episode.  
- Pygame displays the real-time game frame, showing the progress of the agent during training.  
- The trained agent can serve as a foundation for reinforcement learning experiments or enhancements, such as double DQN or experience replay.  
"""


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
    """
    A Deep Q-Network (DQN) model for reinforcement learning.

    This class defines a simple feedforward neural network used to approximate 
    the Q-values of given states and actions.

    Attributes:
        fc (torch.nn.Sequential): The sequential network consisting of a fully connected 
                                hidden layer with ReLU activation and an output layer 
                                predicting Q-values for each action.

    Methods:
        forward(x):
            Computes the forward pass through the network to predict Q-values for the given input state.
    """
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
    """
    Selects an action using an epsilon-greedy policy.

    Args:
        state (numpy.ndarray): The current state represented as an array.
        policy_net (DQN): The deep Q-network used to predict Q-values.
        epsilon (float): The exploration rate determining the probability of selecting a random action.

    Returns:
        int: The action chosen, either randomly or based on the policy network's prediction.
    """
    if random.random() < epsilon:
        return random.choice(legal_actions)
    with torch.no_grad():
        state = torch.FloatTensor(state).unsqueeze(0)
        return legal_actions[policy_net(state).argmax(dim=1).item()]

def render():
    """
    Renders the current game frame using Pygame.

    This function fetches the current game screen, converts it into a Pygame surface, 
    and displays it on the initialized Pygame window.
    """
    pygame.event.pump()
    rgb_array = ale.getScreenRGB()
    surface = pygame.surfarray.make_surface(np.transpose(rgb_array, (1, 0, 2)))
    screen.blit(surface, (0, 0))
    pygame.display.flip()


def train_dqn(num_episodes=1000, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.96):
    """
    Trains the deep Q-network using the given game environment and parameters.

    Args:
        num_episodes (int, optional): The number of episodes to train for. Defaults to 1000.
        gamma (float, optional): The discount factor for future rewards. Defaults to 0.99.
        epsilon (float, optional): The initial exploration rate. Defaults to 1.0.
        epsilon_min (float, optional): The minimum exploration rate. Defaults to 0.01.
        epsilon_decay (float, optional): The decay factor for epsilon per episode. Defaults to 0.96.

    This function performs the following steps:
    - Initializes the game and network.
    - Runs episodes of the game, using epsilon-greedy action selection.
    - Updates the network using TD learning and backpropagation.
    - Adjusts the exploration rate after each episode.
    """
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
