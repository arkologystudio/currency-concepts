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
    mean = params["avg_transaction_ammount"]
    loans_active = params["loans_active"]
    interest_rate = params["interest_rate"]
    payment_increment = params["payment_increment"]

    for i in range(nAgents):
        recipient = random.randint(0, nAgents)
        ammount = int(random.normal(mean, mean/2))
        #ammount = int(random.randint(mean/2, mean*2))
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
                    payment = int(loan_ammount / payment_increment)
                    loans = np.append(loans, [[p, i, loan_ammount, payment]], axis=0) # [lender, borrower, ammount, payment]
                    break

    

    return {"balances": balances, "loans": loans}      


def p_loan_payments(params, substep, state_history, previous_state):  

    balances = previous_state["balances"]
    loans = previous_state["loans"] # [lender, borrower, ammount, payment]

    loans_active = params["loans_active"]

    # Loop through loan arr and init payments
   
    

    if loans_active:
        
        n_loans = loans.shape[0]
        
        for i in range(n_loans):

            lender = loans[i][0]
            borrower = loans[i][1]
            ammount = loans[i][2]
            payment = loans[i][3]

            if payment < balances[borrower] * 2: # Can borrower can afford to make loan repayment
                if(ammount > payment): 
                    balances[lender] += payment
                    balances[borrower] -= payment
                    loans[i][2] -= payment
                    
                else: # make final payment
                    balances[lender] += ammount # pay final due
                    balances[borrower] -= ammount

                    loans[i][3] = 0
                
        
    # df_loans = DataFrame(n_loans)
    # st.line_chart(df_loans)

    return {"balances": balances, "loans": loans}


# STATE UPDATE FUNCTIONS

def s_balances(params, substep, state_history, previous_state, policy_input):
    return "balances", policy_input["balances"]

def s_loans(params, substep, state_history, previous_state, policy_input):
    return "loans", policy_input["loans"]