import math
import numpy as np
import numpy.random as random
from pandas import DataFrame
from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend

import streamlit as st

# POLICY FUNCTIONS

def p_transact(params, substep, state_history, previous_state):  
    
    balances = previous_state["balances"]
    loans = previous_state["loans"]

    nAgents = params["n_agents"]
    max_transaction_amount = params["max_transaction_amount"]
    loans_active = params["loans_active"]
    interest_rate = params["interest_rate"]
    n_instalments = params["n_instalments"]

    for i in range(nAgents):
        recipient = random.randint(0, nAgents)
        #ammount = int(random.normal(mean, mean/2))
        ammount = int(random.randint(10, max_transaction_amount))
        if balances[i] > ammount*2:

            balances[i] -= ammount
            balances[recipient] += ammount
                   
        
        elif loans_active: # Loan
            
            for p in range(nAgents): # 1. find wealthy lender
                
                if ammount*5 < balances[p]: # if lender is 'wealthy' enough
                    # 2. Subtract loan ammount from lender & make payment
                    balances[p] -= ammount
                    balances[recipient] += ammount 
                    # 3. Record loan
                    loan_ammount = int(ammount*(1+interest_rate))
                    payment = int(loan_ammount / n_instalments)
                    loans = np.append(loans, [[p, i, loan_ammount, payment]], axis=0) # [lender, borrower, ammount, payment]
                    break


    return {"balances": balances, "loans": loans}      


def p_loan_payments(params, substep, state_history, previous_state):  

    balances = previous_state["balances"]
    loans = previous_state["loans"] # [lender, borrower, ammount, payment]

    loans_active = params["loans_active"]

    if loans_active:
        n_loans = loans.shape[0]
        for i in range(n_loans):

            lender = loans[i][0]
            borrower = loans[i][1]
            ammount = loans[i][2]
            payment = loans[i][3]

            if payment != 0 and (payment < balances[borrower] * 2): # Can borrower can afford to make loan repayment  
                if(ammount > payment): 
                    balances[lender] += payment
                    balances[borrower] -= payment
                    loans[i][2] -= payment     
                elif balances[borrower] > ammount: # make final payment
                    balances[lender] += ammount # pay final due
                    balances[borrower] -= ammount

                    loans[i][3] = 0
                    loans[i][2] = 0
                    

    return {"balances": balances, "loans": loans}


# STATE UPDATE FUNCTIONS

def s_balances(params, substep, state_history, previous_state, policy_input):
    return "balances", policy_input["balances"]

def s_loans(params, substep, state_history, previous_state, policy_input):
    return "loans", policy_input["loans"]