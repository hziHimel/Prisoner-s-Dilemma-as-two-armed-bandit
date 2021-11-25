import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


"""
Let Confess == 'C' == 0
    Deny    == 'D' == 1
    
Let think this as a 2-armed bandit problem. For given reward which arm should I select?

Reward configuration:
    ('C', 'C') == (-3, -3)
    ('C', 'D') == (-5, 0)
    ('D', 'C') == (0, -5)
    ('D', 'D') == (-1, -1)

"""

class RL_agent:
    def __init__(self, iters, opponent_action = 0, opponent_action_type = 'fixed'):
        self.iters = iters      # How many times the loop will continue in an episode
        self.opponent_action = opponent_action
        self.k = 2    # 2 armed bandit
        self.eps = 0.01     # Epsilod-greedy approach
        self.k_reward = np.zeros(self.k)        # Average reward for each arm after iterations
        self.reward_iters = np.zeros(self.iters)    # Average total reward for each iterations
        self.n = 0      
        self.mean_reward = 0
        self.opponent_action_type = opponent_action_type    # Opponent agent behaves randomly or a fixed behaviour
        self.k_n = np.zeros(self.k) # How many times each 
        
    
    def updateParameters(self):
        randN = np.random.rand() # Generating random number from gaussian distribution to choose between exploration and exploitation
        
        
        if randN < self.eps:
            a = np.random.choice(self.k)    # Selecting a random action
        else:
            a = np.argmax(self.k_reward)    # Selecting greedy action
            
            
        if self.opponent_action_type == 'random':
            self.opponent_action = np.random.choice([0,1])
            
            
        if self.opponent_action == 0:       # Opponent confesses
            reward = -3 if a == 0 else 0    # reward will be -3 if agent itself also confesses, 0 otherwise
        elif self.opponent_action == 1:     # Opponent denies
            reward = -5 if a == 0 else -1   # reward will be -5 if agent itself confesses, -1 otherwise
        
        self.n += 1
        self.k_n[a] += 1
        
        self.mean_reward = self.mean_reward + (reward - self.mean_reward) / self.n
        self.k_reward[a] = self.k_reward[a] + (reward - self.k_reward[a]) / self.k_n[a]
    
    def run(self):      # Update paramaters and rewards
        for i in range(self.iters):
            self.updateParameters()
            self.reward_iters[i] = self.mean_reward
            
    def reset(self):        # Reset all the parameters
        self.n = 0
        self.k_n = np.zeros(self.k)
        self.mean_reward = 0
        self.reward_iters = np.zeros(self.iters)
        self.k_reward = np.zeros(self.k)


def simulate(opponent_action):      # Simulate episodes
    k = 2 
    iters = 1000
    episodes = [1, 10, 1000]
    
    episode_rewards = np.zeros(iters)
    episode_selections = np.zeros(k)
    opponent = ['confess', 'deny', 'behave randomly']
    
    fig, ax = plt.subplots(2, 2, figsize=(16,16))
    
    for idx, e in enumerate(episodes):
        for i in range(e):
            if opponent_action == 2:
                opponent_action_type = 'random'
            else:
                opponent_action_type = 'fixed'
                
            episode = RL_agent(iters=iters, opponent_action=opponent_action, opponent_action_type=opponent_action_type)
            episode.run()

            episode_rewards = episode_rewards + (episode.reward_iters - episode_rewards) / (i + 1)
            episode_selections = episode_selections + (episode.k_n - episode_selections) / (i + 1)

        if idx < 2:
            idx = 0, idx%2
        else:
            idx = 1, idx%2
        ax[idx].title.set_text(f'Number of episode: {e}')
        ax[idx].set_xlabel('Iterations')
        ax[idx].set_ylabel('Average Reward')
        ax[idx].plot(episode_rewards)

        episode.reset()
    idx = idx[0], idx[1]+1
    ax[idx].bar(np.linspace(0, k-1, k), episode_selections, width=0.2, color='b')
    ax[idx].title.set_text('Taken Action')
    ax[idx].set_xlabel('Action')
    ax[idx].set_ylabel('Number of actions taken')
    
    fig.suptitle(f'Simulation when opponent decides to {opponent[opponent_action]}', fontsize=16)
    # fig.show()
    print(f'Our Agent has decided to confess {episode_selections[0]} times and decided to deny {episode_selections[1]} times when opponent decides to {opponent[opponent_action]}')
        
        

opponent = ['confess', 'deny', 'random']
for i, v in enumerate(opponent):
    simulate(i)
plt.show()