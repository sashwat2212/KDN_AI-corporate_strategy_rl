import numpy as np
import random
import gym
from gym import spaces


class CorporateStrategyEnv(gym.Env):
    def __init__(self, num_companies=2, initial_capital=1000, initial_market_share=50):
        super(CorporateStrategyEnv, self).__init__()
        self.num_companies = num_companies
        self.initial_capital = initial_capital
        self.initial_market_share = initial_market_share
        
        self.state = np.array([
            [initial_capital, initial_market_share] for _ in range(num_companies)
        ], dtype=np.float32)
        
        self.action_space = spaces.Discrete(4)
        
        self.observation_space = spaces.Box(
            low=np.array([[0, 0] for _ in range(num_companies)], dtype=np.float32),
            high=np.array([[np.inf, 100] for _ in range(num_companies)], dtype=np.float32),
            dtype=np.float32
        )

    def step(self, actions):
        rewards = np.zeros(self.num_companies)
        market_fluctuation = random.uniform(-0.05, 0.05)  
        
        for i, action in enumerate(actions):
            capital, market_share = self.state[i]
            
            if action == 0:  # Invest in R&D
                capital -= 50
                market_share += 5
                rewards[i] = 10  # Investment may yield long-term gains
            
            elif action == 1:  # Marketing
                capital -= 30
                market_share += 3
                rewards[i] = 7 # Marketing may yield short-term gains
                
            elif action == 2:  # Pricing Strategy
                market_share += random.choice([-2, 2])  # Risk-reward tradeoff
                rewards[i] = 5 if market_share > self.initial_market_share else -5 
                
            elif action == 3:  # Acquisition (if enough capital - 200)
                if capital > 200:
                    capital -= 200
                    market_share += 10
                    rewards[i] = 15
                else:
                    rewards[i] = -10  # Penalty for attempting acquisition with low capital
                    
            
            market_share *= (1 + market_fluctuation)

            
            market_share = max(0, min(100, market_share))
            
            
            self.state[i] = [capital, market_share]
        
        return self.state, rewards, False, {}

    
    def reset(self):
        self.state = np.array([
            [self.initial_capital, self.initial_market_share] for _ in range(self.num_companies)
        ], dtype=np.float32)
        return self.state

    
    def render(self):
        for i, (capital, market_share) in enumerate(self.state):
            print(f"Company {i}: Capital = {capital}, Market Share = {market_share}%")



