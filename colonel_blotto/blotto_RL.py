import pyspiel
import numpy as np
from open_spiel.python import rl_environment
from open_spiel.python.algorithms import random_agent
from open_spiel.python.algorithms import tabular_qlearner
from open_spiel.python import rl_tools

MAX_EPISODES = 1000000
NUM_PLAYERS = 2
NUM_FIELDS = 3
NUM_COINS = 10

np.random.seed(1)

settings = {'players' : NUM_PLAYERS, 'fields' : NUM_FIELDS, 'coins' : NUM_COINS}
environment = rl_environment.Environment('blotto', **settings)
num_actions = environment.action_spec()['num_actions']
print("Possible Actions:", num_actions)
rl_agent = tabular_qlearner.QLearner(player_id=0, num_actions=num_actions, epsilon_schedule=rl_tools.ConstantSchedule(0.2))
opponent = random_agent.RandomAgent(player_id=1, num_actions=num_actions)

won_games = [0,0]
rl_won = []
opp_won = []

last_probs = None

episode = 0
while episode < MAX_EPISODES:
    episode += 1
    print("EPISODE", episode)

    time_step = environment.reset() #initial step per episode

    while not time_step.last():
        rl_step = rl_agent.step(time_step)
        opp_step = opponent.step(time_step)

        rl_action = rl_step.action
        opp_action = opp_step.action

        last_probs = rl_step

        print('RL', rl_action, ':', environment.get_state.action_to_string(0, rl_action))
        print('Opp', opp_action, ':', environment.get_state.action_to_string(1, opp_action))
        actions = [rl_action, opp_action]

        time_step = environment.step(actions)

    #Episode over, step both agents with final state
    rl_agent.step(time_step)
    opponent.step(time_step)

    #print(environment.get_state)
    rewards = environment.get_state.returns()
    print ("Rewards:", rewards)
    
    won_games[0] += rewards[0] if rewards[0] > 0 else 0
    won_games[1] += rewards[1] if rewards[1] > 0 else 0

    rl_won.append(won_games[0])
    opp_won.append(won_games[1])

    print()
    
print("\nWON Games")
print("RL Agent:", int(won_games[0]))
print('Opponent:', int(won_games[1]))
print(last_probs)
#print(len(rl_agent._q_values))
#print(rl_agent._q_values.keys())
print(rl_agent._q_values['[0.0]'])
q_list = []
for act in rl_agent._q_values['[0.0]'].keys():
    q_val = rl_agent._q_values['[0.0]'][act]
    q_list.append(q_val)

done = set()
for val in sorted(q_list, reverse=True):
    if val in done:
        continue

    done.add(val)

    for act in rl_agent._q_values['[0.0]'].keys():
        if val == rl_agent._q_values['[0.0]'][act]:
            act_string = environment.get_state.action_to_string(0, act)
            print(val, act, act_string)


#print()
#print('Won Trend')
#print('RL Agent:', rl_won)
#print('Opponent:', opp_won)