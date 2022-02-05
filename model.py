import numpy as np
import numpy.random as random
from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend


# POLICY FUNCTIONS

def p_transact(params, substep, state_history, previous_state):  
    
    balances = previous_state["balances"]
    loans = previous_state["loans"]

    nAgents = params["n_agents"]
    mean = params["avg_transaction_ammount"]
    interest = params["interest"]
    interest_rate = params["interest_rate"]
    payment_increment = params["payment_increment"]

    for i in range(nAgents):
        recipient = random.randint(0, nAgents, dtype=np.uint16)
        ammount = random.normal(mean, mean/10)

        if balances[i] > ammount*2:
            balances[i] -= ammount
            balances[recipient] += ammount
        elif interest: # Loan
            
            for p in range(nAgents): # 1. find wealthy lender
                if ammount*10 < balances[p]: # if lender is 'wealthy' enough
                    # 2. Subtract loan ammount from lender & make payment
                    balances[p] -= ammount
                    balances[recipient] += ammount 
                    # 3. Record loan
                    loan_ammount = ammount*(1+interest_rate)
                    payment = loan_ammount / payment_increment
                    loans = np.append(loans, [[p, i, loan_ammount, payment]], axis=0) # [lender, borrower, ammount, payment]
                    break


    return {"balances": balances, "loans": loans}      



# STATE UPDATE FUNCTIONS

def s_balances(params, substep, state_history, previorus_state, policy_input):
    return "balances", policy_input["balances"]

def s_loans(params, substep, state_history, previous_state, policy_input):
    return "loans", policy_input["loans"]