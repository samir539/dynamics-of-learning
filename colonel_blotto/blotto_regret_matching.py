import numpy as np
import random 
np.set_printoptions(suppress=True)
from itertools import combinations
import itertools
from matplotlib import pyplot as plt
from tqdm import tqdm

battlefield_num = 3
num_actions = 21
num_players = 2
S = 5

battlefields = np.zeros(battlefield_num)
regret_sum = np.zeros((num_players,num_actions))
strategy = np.zeros((num_players,num_actions))
strategy_sum = np.zeros((num_players,num_actions))
opp_strat = np.array([0.9,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])


def getStrategy(player):
    """
    obtain the strategy for a given player
    :param player: integer, player 1 [0] or player 2 [1]
    :return strategy: array of the given players strategy
    """
    normalising_sum = 0
    for i in range(num_actions):
        if regret_sum[player,i] > 0:
            strategy[player,i] = regret_sum[player,i]
        else:
            strategy[player,i] = 0
        normalising_sum = normalising_sum + strategy[player,i]
    for j in range(num_actions):                    #one could use numpy slices to get rid of loop
        if normalising_sum > 0:
            strategy[player,j] /= normalising_sum
        else:
            strategy[player,j] = 1/num_actions
        strategy_sum[player,j] += strategy[player,j]
    return strategy[player,:]


def getAction(strategy):
    rand_val = random.uniform(0,1)
    a = 0
    cumulative_prob = 0
    while(a < num_actions-1):
        cumulative_prob = cumulative_prob + strategy[a]
        if (rand_val < cumulative_prob):
            return a
        a = a + 1
    return a


def generate_ids(S,N):
    """
    generate list of all possible actions a commander can take given S soliders and N battlefields
    :param S: number of soliders
    :param N: number of battlefields
    :return IDarray: Numpy array of all possible actions with the index being equal to their ID
    """
    space = list(range(S+1)) * N
    ID_array = np.array(list(set(i for i in itertools.permutations(space,N) if sum(i) == S)))
    return ID_array




def utility(id_p1,id_p2,idlist):
    """
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

def getUtility(otherAction,id_list):
    """
    give table of utilities such that given otheraction we get all the payoffs of everything that could have been played against it
    """
    utilityarray = np.zeros(num_actions)
    for i in range(len(id_list)):
        utilityarray[i] = utility(i,otherAction,id_list)
    return utilityarray




def getaveragestrat(player):
    avgStrat = np.zeros(num_actions)
    normalising_sum = 0
    for i in range(num_actions):
        normalising_sum += strategy_sum[player][i]
    for j in range(num_actions):
        if normalising_sum > 0:
            avgStrat[j] = strategy_sum[player][j]/normalising_sum
        else:
            avgStrat[j] = 1.0/num_actions
    return avgStrat



def training(iterations):
    global regret_sum
    strategy_sum_blotto_list = []
    strategy_sum_boba_list = []
    norm_list_blotto = []
    norm_list_boba = []
    for i in tqdm(range(iterations)):
        blotto = 0
        boba = 1
        blotto_action = getAction(getStrategy(0))
        boba_fet_action = getAction(getStrategy(1))
        id_list = generate_ids(S,battlefield_num)
        util_val_blotto = utility(blotto_action,boba_fet_action,id_list)
        util_val_boba = utility(boba_fet_action,blotto_action,id_list)
        util_array_blotto = getUtility(boba_fet_action,generate_ids(S,battlefield_num))
        util_array_boba = getUtility(blotto_action,generate_ids(S,battlefield_num))
        regret_blotto = util_array_blotto - util_array_blotto[blotto_action]
        regret_boba = util_array_boba - util_array_boba[boba_fet_action]
        #alternate regret matching
        if i%2 == 0:
            regret_sum[blotto] = regret_sum[blotto] + (regret_blotto)
        elif i%2 == 1:
            regret_sum[boba] = regret_sum[boba] + (regret_boba)
        a = getaveragestrat(0)
        b = np.linalg.norm(a)
        norm_list_blotto.append(b)

        c = getaveragestrat(1)
        d = np.linalg.norm(c)
        norm_list_boba.append(d)
    return norm_list_blotto,norm_list_boba
iterations = 100000
norm_list,norm_list_boba = training(iterations)
norm_list_array = np.array(norm_list)
print("p1",getaveragestrat(0))
print("p2",getaveragestrat(1))
x_vals = np.linspace(0,iterations,iterations)
print(x_vals.shape,norm_list_array.shape)
plt.plot(x_vals,norm_list_boba, color="red")
plt.tick_params(axis='both', labelsize=22)
plt.xlabel("Number of Iterations", fontsize=18)
plt.ylabel("2-Norm of Average Strategy ",fontsize=18)
# plt.plot(x_vals,norm_list_boba)
plt.show()


            







