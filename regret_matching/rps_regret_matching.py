import numpy as np
import random 
from tqdm import tqdm

np.set_printoptions(suppress=True)
#define variables
rock = 0
paper = 1
scissors = 2
num_actions = 3

#arrays
regretSum = np.zeros(num_actions, dtype=np.float64)
strategy = np.zeros(num_actions, dtype=np.float64)
strategySum = np.zeros(num_actions)
oppStrategy = np.array([0.333333,0.33333,0.3333])
# regretSum = np.array([1,3,2])
#get current mixed strategy with regret matching
def getStrategy():
    normalising_sum = 0
    for i in range(num_actions):
        if regretSum[i] > 0:
            strategy[i] = regretSum[i]
        else:
            strategy[i] = 0
        # print("this is the stratergy pre divide", strategy)
        normalising_sum = normalising_sum + strategy[i]
    for j in range(num_actions):
        if normalising_sum > 0:
            strategy[j] /= normalising_sum
        else:
            strategy[j] = 1.0/num_actions
        strategySum[j] += strategy[j]
    return strategy
# print(getStrategy())

#get specific action randomly chosen according to mixed strategy distribution
def getAction(strategy):
    rand_val = random.uniform(0,1)
    a = 0
    cumulative_prob = 0
    # print("this is stratergy",strategy)
    while(a < num_actions-1):
        cumulative_prob = cumulative_prob + strategy[a]
        if (rand_val < cumulative_prob):
            return a
        a = a + 1
    return a


#find utilities
def getUtility(myAction,otherAction):
    """
    :return regretarray:
    """
    utilityarray = np.zeros(num_actions)
    utilityarray[otherAction] = 0
    if otherAction == num_actions -1:
        utilityarray[0] = 1
    else:
        utilityarray[otherAction + 1] = 1
    
    if otherAction == 0:
        utilityarray[num_actions-1] = -1
    else:
        utilityarray[otherAction-1] = -1
    return utilityarray
# print(getUtility(0,1))
#get regret array
def getRegretArray(myAction,otherAction):
    actionUilitity = getUtility(myAction,otherAction)
    # print("this is the utility", actionUilitity)
    regretArray = np.zeros(num_actions)
    for i in range(num_actions):
        regretArray[i] += actionUilitity[i] - actionUilitity[myAction]
    return regretArray

# def regretappend(regretSum,regretArray):
    print("this is the regret sum",regretSum)
    print("this is the regret array",regretArray)
    regretSum = regretSum + regretArray
    print("this is regretsum",regretSum)
    return regretSum

#train
# def train(iterations,regretSum):
#     for i in range(iterations):
#         strategy = getStrategy()
#         p1_action = getAction(strategy)
#         p2_action = getAction(oppStrategy)
#         regret = getRegretArray(p1_action,p2_action)
#         regretSum = regretSum + regret
#     return strategy
# l = train(4,regretSum)
# print(l)

# def train(iterations): #this one works
#     global regretSum
#     actionUtility = np.zeros(num_actions)
#     for i in range(iterations):
#         strategy = getStrategy()
#         myAction = getAction(strategy)
#         otherAction = getAction(oppStrategy)
        
#         actionUtility[otherAction] = 0
#         actionUtility[(otherAction + 1)% num_actions] = 1
#         actionUtility[(otherAction - 1)% num_actions] = -1

#         regretSum = regretSum + (actionUtility - actionUtility[myAction])

def train(iterations):
    global regretSum
    for i in tqdm(range(iterations)):
        strategy = getStrategy()
        myAction = getAction(strategy)
        print("four action", myAction)
        otherAction = getAction(oppStrategy)
        print("other action", otherAction)
        utilityarray = getUtility(myAction,otherAction)
        print("this is the utilityarray,",utilityarray)
        print("these are the regrets", utilityarray - utilityarray[myAction])
        regretSum = regretSum + (utilityarray - utilityarray[myAction])



def getaveragestrat():
    avgStrat = np.zeros(num_actions)
    normalising_sum = 0
    for i in range(num_actions):
        normalising_sum += strategySum[i]
    for j in range(num_actions):
        if normalising_sum > 0:
            avgStrat[j] = strategySum[j]/normalising_sum
        else:
            avgStrat[j] = 1/num_actions
    return avgStrat


train(2)
print(getaveragestrat())
# b = train(100,regretSum)
# print(b)
# print(getaveragestrat())



# print("this is regret sum before",regretSum)
# printstrat = getStrategy()
# p1 = getAction(strategy)
# p2 = getAction(oppStrategy)
# regretarrayprint = getRegretArray(p1,p2)
# print("this is the regret array",regretarrayprint)
# regretSum += regretarrayprint
# print("this is the regretsum after",regretSum)

# print(printstrat)
# print(p1)
# print(p2)
# print(regretarrayprint)

# print(getStrategy())
# p1 = getAction(strategy)
# p2 = getAction(oppStrategy)
# regretarrayprint = getRegretArray(p1,p2)
# print("this is the regret array",regretarrayprint)
# regretSum += regretarrayprint
# print("this is the regretsum after",regretSum)
# print(getStrategy())
