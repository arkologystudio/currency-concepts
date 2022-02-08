"""Experiment Configuration"""

# radCAD Modules
from radcad import Model, Simulation, Experiment

import numpy as np
from models.interest_inequality.interest_inequality import p_transact, p_loan_payments, s_balances, s_loans


params = {
    "n_agents": [50],
    "max_transaction_amount": [500],
    "loans_active": [False],
    "interest_rate": [0.075],
    "n_instalments": [7],
}

initial_state = {
    "balances": np.full(params["n_agents"][0], 1000,  dtype=int), # set starting balances 
    # "balances": np.random.randint(1, 20000, params["n_agents"][0]), # randomize starting balances
    "loans": np.empty((0, 4), np.int16) # [lender, borrower, ammount, payment]
}

state_update_blocks = [
    {
        "policies": {
            "transactions": p_transact,  
        },
        "variables": {
            "balances": s_balances,
            "loans": s_loans
        },
    },
    {
        "policies": {
            "loan_payments": p_loan_payments,
        },
        "variables": {
             "balances": s_balances,
             "loans": s_loans
        }
    }
]

TIMESTEPS = 60 # default
RUNS = 1

model = Model(
    initial_state=initial_state,
    state_update_blocks=state_update_blocks,
    params=params,
)
simulation_interest_inequality = Simulation(model=model, timesteps=TIMESTEPS, runs=RUNS)