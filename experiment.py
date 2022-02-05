"""Experiment Configuration"""

# radCAD Modules
from radcad import Model, Simulation, Experiment

import numpy as np
from model import p_transact, s_balances, s_loans


params = {
    "n_agents": [100],
    "avg_transaction_ammount": [20],
    "loan_type": [None],
    "Interest": [False],
    "interest_rate": [0.05],
    "payment_increment": [30],
}

initial_state = {
    "balances": np.random.randint(450, 550, params["n_agents"][0]), # randomize starting balances
    "loans": np.empty((0, 4), dtype=float) # [lender, borrower, ammount, payment]
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