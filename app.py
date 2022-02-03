import streamlit as st

import numpy as np
import pandas as pd
import time
import io

import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

import matplotlib.animation as animation
import streamlit.components.v1 as components


"""
# Currency Concepts - Example Model

### cadCAD model demonstrating ..

#### Created by Arkology Studio

...


"""

# radCAD Model
from model import p_transact, s_balance

# radCAD Modules
from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend

n_agents = st.slider('Number of agents', 10, 200, 100)  # min: 0h, max: 23h, default: 17h
avg_transaction_ammount = st.slider('AVG transaction ammount', 10, 100, 20)
# Experiment

params = {
    "n_agents": [n_agents],
    "avg_transaction_ammount": [avg_transaction_ammount]
}

initial_state = {
    "agents": np.random.randint(450, 550, params["n_agents"][0]), # randomize starting balances
    
}

state_update_blocks = [
    {
        "policies": {
            "transactions": p_transact,
        },
        "variables": {
            "agents": s_balance,
        },
    }
]


TIMESTEPS = 10
RUNS = 1

model = Model(
    initial_state=initial_state,
    state_update_blocks=state_update_blocks,
    params=params,
)
simulation = Simulation(model=model, timesteps=TIMESTEPS, runs=RUNS)



if __name__ == "__main__":
    result = simulation.run()

    df = pd.DataFrame(
        result
    )
    # st.dataframe(df)


    # Expand agents
    df_2 = df.apply(lambda row: list(row.agents), axis=1, result_type='expand')
    #st.dataframe(df_2)



    # ANIMATE

    #fig = plt.figure()
    fig, ax = plt.subplots(1, 1)
    plot = ax.bar([agent for agent in df_2], df_2.iloc[0])
    ax.set(xlabel='Agents', ylabel='Balance (USD)',
       title='Account Balances')
    

    st.subheader('Market Simulator')

    def animate_func(timestep):
        
        # Sort ??
        #df_2.sort_values(by = timestep, axis=1, ascending = False)
        #df_2.sort_index(inplace=True)

        ax.clear()
        
        state = df_2.iloc[timestep]
        plot = ax.bar([agent for agent in df_2], state)
        ax.set_ylim([0, 1000])
        return [plot]

    anim = animation.FuncAnimation(
        fig,
        animate_func,
        frames=TIMESTEPS,
        interval=200,  # in ms
    )

    #plt.show()

    components.html(anim.to_jshtml(), height=800)