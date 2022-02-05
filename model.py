import numpy as np
import numpy.random as random
from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend


# POLICY FUNCTIONS

def p_transact(params, substep, state_history, previous_state):  
    
    agentBalances = previous_state["agents"]

    nAgents = params["n_agents"]
    mean = params["avg_transaction_ammount"]

    for i in range(nAgents):
        recipient = random.randint(0, nAgents, dtype=np.uint16)
        ammount = random.normal(mean, mean/10)

        if agentBalances[i] > ammount:
            agentBalances[i] -= ammount
            agentBalances[recipient] += ammount


    return {"balances": agentBalances}      



# STATE UPDATE FUNCTIONS

def s_balance(params, substep, state_history, previous_state, policy_input):
    return "agents", policy_input["balances"]

def s_gini(params, substep, state_history, previous_state, policy_input):
    return "gini", policy_input["gini"]