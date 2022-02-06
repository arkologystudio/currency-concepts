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
st.text("Agent-based radCAD/cadCAD simulation of a simple market economy.")
st.text("The model aims to demonstrate the effect of interest-bearing loans")
st.text("on wealth inequality indeces.")


# Parameter Inputs

st.subheader("Simulation parameters:")
col1, col2, col3 = st.columns(3)
with col1:
    n_agents = st.slider('Number of agents', 10, 200, 30, 10)  # params: min, max, default, step
    avg_transaction_ammount = st.slider('AVG transaction ammount', 50, 500, 200, 50)
    st.markdown("**Simulation time horizon:**")
    TIMESTEPS = st.slider("Days: ", 14, 28*12, 28, 14)
    

with col2:
    st.subheader("")
    
with col3:
    st.subheader("")
    interest_rate = st.slider("Interets Rate (%):", 1.0, 15.0, 5.0, 1.0) / 100
    option = st.selectbox("Loans:", ('Inactive', 'Active'), 0, help="If loans are activated, 'poorer' agents will loan money from 'wealthier' ones.")
    loans_active = False # default
    if option == 'Active': 
        print("Loans Activated")
        loans_active = True


# Simulation & Post-processing
if __name__ == "__main__":


    transactionChart = st.checkbox("Show market simulator") 
    st.text("(Note: increases load time significantly")
    st.text("--------------------------------")

    simulate = st.button("Simulate")

    # SIMULATE
    if simulate:

        # Update Simulation Parameters based on user input
        simulation.model.params.update({
            "n_agents": [n_agents], 
            "avg_transaction_ammount": [avg_transaction_ammount],
            "loans_active": [loans_active],
            "interest_rate": [interest_rate]
        })

        simulation.model.initial_state.update({
            "balances": np.full(n_agents, 500,  dtype=int)
        })

        # RUN SIMULATION
        simulation.timesteps = TIMESTEPS
        st.write("Running simulation ..")
        result = simulation.run()

        df = pd.DataFrame(result)
        

        # DATA POST-PROCESSING
        st.subheader("Balances - DataFrame")
        df_balance_spread = expand(df)
        st.dataframe(df_balance_spread)


        # PLOT RESULTS
        if transactionChart:
            st.subheader("Market Simulator:")
            chart_market_animation(df_balance_spread, TIMESTEPS)

        st.subheader("Gini Coefficient")
        df_gini = gini_index(df, TIMESTEPS)
        chart_gini(df_gini)

            

        
        
    

    

    