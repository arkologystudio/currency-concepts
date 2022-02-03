import numpy as np
import random

from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend


# POLICY FUNCTIONS

def p_transact(params, substep, state_history, previous_state):  
    
    agentBalances = previous_state["agents"]
    nAgents = params["n_agents"]

    for i in range(nAgents):
        recipient = random.randint(0, nAgents-1)
        ammount = random.randint(10, min(100, agentBalances[i]))

        agentBalances[i] -= ammount
        agentBalances[recipient] += ammount


    return {"balances": agentBalances}      


# STATE UPDATE FUNCTIONS

def s_balance(params, substep, state_history, previous_state, policy_input):
    return "agents", policy_input["balances"]

