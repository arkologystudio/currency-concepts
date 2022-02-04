"""Experiment Configuration"""

# radCAD Modules
from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend

import numpy as np
from model import *


params = {
    "n_agents": [100],
    "avg_transaction_ammount": [20],
    "loan_type": [None],
}

initial_state = {
    "agents": np.random.randint(450, 550, params["n_agents"][0]), # randomize starting balances
    "gini": 0
    
}

state_update_blocks = [
    {
        "policies": {
            "transactions": p_transact,
            "gini": p_gini,
        },
        "variables": {
            "agents": s_balance,
            "gini": s_gini,
        },
    }
]

TIMESTEPS = 60
RUNS = 1

model = Model(
    initial_state=initial_state,
    state_update_blocks=state_update_blocks,
    params=params,
)
simulation = Simulation(model=model, timesteps=TIMESTEPS, runs=RUNS)