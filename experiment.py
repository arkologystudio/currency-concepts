"""Experiment Configuration"""

# radCAD Modules
from radcad import Model, Simulation, Experiment

import numpy as np
from model import p_transact, p_loan_payments, s_balances, s_loans


params = {
    "n_agents": [50],
    "avg_transaction_ammount": [50],
    "loan_type": [None],
    "Interest": [False],
    "interest_rate": [0.05],
    "payment_increment": [2],
}

initial_state = {
    "balances": np.full(params["n_agents"][0], 500,  dtype=int), # randomize starting balances
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

TIMESTEPS = 30 # default
RUNS = 1

model = Model(
    initial_state=initial_state,
    state_update_blocks=state_update_blocks,
    params=params,
)
simulation = Simulation(model=model, timesteps=TIMESTEPS, runs=RUNS)