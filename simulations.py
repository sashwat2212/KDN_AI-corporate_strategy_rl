import numpy as np
from env import CorporateStrategyEnv
from agents import QLearningAgent
import matplotlib.pyplot as plt
import os

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)  

def train_agents(num_agents=5, num_episodes=1000, max_steps_per_episode=50):
    
    env = CorporateStrategyEnv(num_companies=num_agents)
    
    
    agents = [QLearningAgent() for _ in range(num_agents)]

    for i, agent in enumerate(agents):
        agent.initial_market_share = env.state[i][1]  
    
    
    performance_log = []

    
    for episode in range(num_episodes):
        state = env.reset()  
        total_rewards = np.zeros(num_agents)

        for step in range(max_steps_per_episode):
            actions = [agent.choose_action(state[i]) for i, agent in enumerate(agents)]  
            next_state, rewards, done, _ = env.step(actions)  

            for i, agent in enumerate(agents):
                agent.update_q_table(state[i], actions[i], rewards[i], next_state[i])  
                total_rewards[i] += rewards[i] 

            if done:  
                break
        
        capital = [env.state[i][0] for i in range(num_agents)]  
        market_share = [env.state[i][1] for i in range(num_agents)]  
        performance_log.append([episode, total_rewards, capital, market_share])  
        
        for agent in agents:
            agent.decay_exploration()

        if episode % 100 == 0:
            print(f"Episode {episode}/{num_episodes}, Rewards: {total_rewards}, Capital: {capital}")

    return env, performance_log, agents

env, performance_log, agents = train_agents() 


def plot_performance(performance_log):
    episodes = np.array([log[0] for log in performance_log])
    rewards = np.array([log[1] for log in performance_log])
    
    plt.figure(figsize=(12, 6))
    for i in range(rewards.shape[1]):
        plt.plot(episodes, rewards[:, i], label=f"Agent {i}")
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.title('Agent Performance over Episodes')
    plt.legend()
    plt.savefig(os.path.join(output_dir, "agent_performance.png"))
    plt.close()

plot_performance(performance_log)

def plot_capital_per_episode(performance_log):
    episodes = np.array([log[0] for log in performance_log])
    capital_log = np.array([log[2] for log in performance_log])  
    
    plt.figure(figsize=(12, 6))
    for i in range(len(capital_log[0])):
        capital_per_agent = [capital_log[episode][i] for episode in range(len(episodes))]  
        plt.plot(episodes, capital_per_agent, label=f"Agent {i} Capital")
    plt.xlabel('Episode')
    plt.ylabel('Capital')
    plt.title('Capital Growth Over Episodes')
    plt.legend()
    plt.savefig(os.path.join(output_dir, "capital_growth.png"))
    plt.close()

plot_capital_per_episode(performance_log)

def plot_market_share(performance_log):
    episodes = np.array([log[0] for log in performance_log])
    market_shares = np.array([log[3] for log in performance_log])

    plt.figure(figsize=(12, 6))
    for i in range(market_shares.shape[1]):
        plt.plot(episodes, market_shares[:, i], label=f"Company {i} Market Share")
    plt.xlabel('Episode')
    plt.ylabel('Market Share')
    plt.title('Market Share Over Episodes')
    plt.legend()
    plt.savefig(os.path.join(output_dir, "market_share.png"))
    plt.close()

plot_market_share(performance_log) 


efficiency_scores = []
market_shares = []

for i, agent in enumerate(agents):
    market_share = env.state[i][1]  
    efficiency_score = (market_share - agent.initial_market_share) / (agent.total_spent + 1e-6)
    efficiency_scores.append(efficiency_score)
    market_shares.append(market_share)

print("Efficiency Scores:", efficiency_scores)
print("Market Shares:", market_shares)

np.save("efficiency_scores.npy", efficiency_scores)
np.save("market_shares.npy", market_shares)


