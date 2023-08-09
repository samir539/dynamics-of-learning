from typing import DefaultDict
import numpy as np
import random
import matplotlib.pyplot as plt
from math import comb
np.set_printoptions(suppress=True)
from itertools import combinations
import itertools
from tqdm import tqdm


#Base code structure used update style of RPS implementation from eskehaack
#set parameters of Blotto game
battlefield_num = 3
S = 5 #no. of soliders
num_of_actions = comb(battlefield_num+S-1,battlefield_num-1)

#number of iterations
iterations = 5000

#set parameters of RL model
epsilon = 1.0 # random act chance
gamma = 0.9 #gamma value in q update rule
alpha = 0.1 #alpha in q update rule [learning rate]
lookback_amount = 2 #the state 
reward = 0.1 #reward

#Init
AI_wins = 0 #player 2
Random_player = 0 #player 1
total_games = 0 
draws = 0
game_outcome = 0

#init qtable
q_values = DefaultDict(lambda:[1/num_of_actions]*num_of_actions)    #works as desired

# Arrays to collect statistics for plots
y_vals_AI = np.array([])
y_vals_Random = np.array([])

#translate each action into an index for q vals dict
def generate_ids(S,N):

    """
    generate list of all possible actions a commander can take given S soliders and N battlefields
    :param S: number of soliders
    :param N: number of battlefields
    :return IDarray: Numpy array of all possible actions with the index being equal to their ID
    """
    space = list(range(S+1)) * N
    ID_array = list(set(i for i in itertools.permutations(space,N) if sum(i) == S))
    return ID_array

list_of_IDs = generate_ids(S, battlefield_num)
dict_of_actions = {i: list_of_IDs[i] for i in range(0,len(list_of_IDs))} #dict of actions

#center val
center_val = 60

def get_key(action_alloc,input_dict):
    """
    take a battlefield soldier allocation profile
    :param action_alloc: the allocation across the battlefields as a tuple
    :param input_dict: the dictionary containing the corresponding key in our case input_dict is list_of_IDs
    """
    key_list = list(input_dict.keys())
    val_list = list(input_dict.values())
    position = val_list.index(action_alloc)
    return position

#determine win or loss or draw
def utility(id_p1,id_p2,idlist):
    """
    :id_p1: action of p1
    :id_p2: action of p2
    :idlist: list of possible actions
    :return utility: the utility of the first inputted player
    """
    battlefields_won = 0
    battlefields_lost = 0
    battlefields_drawn = 0
    for i in range(battlefield_num):
        if idlist[id_p1][i] > idlist[id_p2][i]:
            battlefields_won = battlefields_won + 1
        elif idlist[id_p1][i] == idlist[id_p2][i]:
            battlefields_drawn = battlefields_drawn +1
        elif idlist[id_p1][i] < idlist[id_p2][i]:
            battlefields_lost = battlefields_lost + 1
    if battlefields_won > battlefields_lost:
        return 1
    elif battlefields_won == battlefields_lost or battlefields_drawn == battlefield_num:
        return 0
    else:
        return -1


#function to translate input numbers to string for q vals dict
def get_row(old_inputs):
    input_list = []
    for action_sets in old_inputs:
        for action in action_sets:
            input_list.append(get_key(action,dict_of_actions))
    input_list = str(input_list)
    return input_list




#function for updating the table
def update_table(action1, action2, old_actions):
    global q_values
    value = q_values[get_row(old_actions)][action2]
    new_value = value + alpha * utility(action2,action1,list_of_IDs) * ((reward) + gamma*np.max(state_row)-value)
    q_values[get_row(old_actions)][action2] = new_value




#old actions
#generate two random old actions to intialise the process
old_actions = []
inner_list = []
for j in range(2):

        inner_list.append(random.choice(list_of_IDs))
old_actions.append(inner_list)
inner_list = []
for i in range(2):
        inner_list.append(random.choice(list_of_IDs))
old_actions.append(inner_list)



#agent input
def agent_input():
    number = random.random()
    if epsilon >= number:
        action_alloc = random.choice(list_of_IDs)   #list of IDs really are a list of allocations
        action = get_key(action_alloc,dict_of_actions)
    else:
        state_row_saved = q_values[get_row(old_actions)]
        equal_max_val = [i for i, j in enumerate(state_row_saved) if j == max(state_row_saved)]
        if len(equal_max_val) > 1:
            action = random.choice(equal_max_val)
        else:
            action = equal_max_val[0]
    return action 

def enemy_input():
    action = random.randrange(21)
    return action


for i in tqdm(range(iterations)):
    
    action1 = enemy_input()
    action2 = agent_input()
    epsilon = epsilon*gamma
    game_outcome = utility(action2,action1,list_of_IDs)
    state_row = np.copy(q_values[get_row(old_actions)]) 
    rest_actions = list(range(0,21))
    rest_actions.pop(action2)
    

    update_table(action1,action2,old_actions)
    for j in range(len(rest_actions)):
        update_table(action1,rest_actions[j],old_actions)

    old_actions.append([dict_of_actions[action2],dict_of_actions[action1]])
    del old_actions[0]

    #plotting
    
    

    #collecting stats
    if game_outcome == 1:
        AI_wins += 1
    elif game_outcome == -1:
        Random_player += 1
    elif game_outcome == 0:
        draws += 1
    total_games = total_games + 1
    y_vals_AI = np.append(y_vals_AI, AI_wins)
    y_vals_Random = np.append(y_vals_Random, Random_player)

    

print("AI wins", AI_wins)
print("Random wins", Random_player)
print("draws", draws)
x_vals = np.linspace(0,iterations,iterations)
print(x_vals)
print(y_vals_AI)
print(y_vals_Random)
print(y_vals_AI.shape,y_vals_Random.shape)
plt.plot(x_vals,y_vals_AI, color="red", label="Q-learning Agent")
plt.plot(x_vals,y_vals_Random, color="black", label="Random Agent")
plt.ylabel('Number of Games Won', fontsize=16)
plt.xlabel('Number of Iterations', fontsize=16)
plt.legend(loc="upper left")
plt.show()