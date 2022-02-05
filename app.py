import streamlit as st

import numpy as np
import pandas as pd
from post_processing import expand, gini_index

from visualizations import chart_market_animation, chart_gini

# Experiment simulation configuration
from experiment import simulation



# FRONTEND / INTERFACE

# Introduction
st.title("Currency Concepts | 2022")
st.subheader("Model: Interest-bearing Loans - V.0.1")
st.text("Agent-based radCAD/cadCAD simulation of a simple market economy,")
st.text("which aims to demonstrate the effect of interest-bearing loans")
st.text("on wealth inequality indeces.")


# Parameter Inputs

st.subheader("Simulation parameters:")
col1, col2, col3 = st.columns(3)
with col1:
    n_agents = st.slider('Number of agents', 10, 200, 30, 10)  # params: min, max, default, step
    avg_transaction_ammount = st.slider('AVG transaction ammount', 10, 100, 20, 10)

with col2:
    st.subheader("")
    
with col3:
    st.subheader("")
    st.markdown("**Simulation time horizon:**")
    TIMESTEPS = st.slider("Days: ", 14, 28*12, 28, 14)
    

col1, col2 = st.columns(2)
with col1:
    loan_type = st.selectbox("Loan type:", ('No Interest', 'Interest'))
    interest = False
    if loan_type == 'Interest': 
        interest = True
    
with col2:
    interest_rate = st.slider("Interets Rate (%):", 1.0, 25.0, 3.5, 0.5)



# Update Simultion Parameters based on user input
simulation.model.params.update({
    "n_agents": [n_agents], 
    "avg_transaction_ammount": [avg_transaction_ammount],
    "interest": [interest],
    "interest_rate": [interest_rate]
})

simulation.model.initial_state.update({
    "balances": np.random.randint(450, 550, n_agents)
})


# Simulation & Post-processing
if __name__ == "__main__":

    simulation.timesteps = TIMESTEPS

    # SIMULATE
    if st.button('Simulate'):

        st.write("Running simulation ..")
        result = simulation.run()

        df = pd.DataFrame(result)
        #st.dataframe(df.balances)

        # Post-processing 
        df_balance_spread = expand(df)
        #st.dataframe(df_balance_spread)

        # Plot data:
        st.subheader("Market Simulator")
        chart_market_animation(df_balance_spread, TIMESTEPS)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Gini Index")
            df_gini = gini_index(df, TIMESTEPS)
            chart_gini(df_gini)

        with col2:
            st.subheader("Trade Frequency")
            

        
        
    

    

    