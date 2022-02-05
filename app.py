import streamlit as st

import numpy as np
import pandas as pd
from post_processing import post_processing, gini_index

from visualizations import chart_market_animation, chart_gini

# Experiment simulation configuration
from experiment import simulation



# FRONTEND / INTERFACE

# Introduction
st.title("Currency Concepts V0.01")
st.subheader("Interactive radCAD/cadCAD simulation of a simple market economy.")
st.text("The model aims to demonstrate the effect of interest-bearing loans")
st.text("on wealth inequality indeces.")


# Parameter Inputs

st.subheader("Simulation parameters:")
col1, col2, col3 = st.columns(3)
with col1:
    n_agents = st.slider('Number of agents', 10, 200, 30)  # min: 0h, max: 23h, default: 17h
    avg_transaction_ammount = st.slider('AVG transaction ammount', 10, 100, 20)

with col2:
    st.subheader("")
    
with col3:
    st.subheader("")
    st.markdown("**Simulation time horizon:**")
    TIMESTEPS = st.slider("Days: ", 10, 365, 50)
    

col1, col2 = st.columns(2)
with col1:
    
    loan_type = st.selectbox("Loan type:", ('No Interest', 'Interest'))




# Update Simultion Parameters based on user input
simulation.model.params.update({
    "n_agents": [n_agents], 
    "avg_transaction_ammount": [avg_transaction_ammount],
})

simulation.model.initial_state.update({
    "agents": np.random.randint(450, 550, n_agents)
})


# Simulation & Post-processing
if __name__ == "__main__":

    simulation.timesteps = TIMESTEPS

    # SIMULATE
    if st.button('Simulate'):

        st.write("Running simulation ..")
        result = simulation.run()

        df = pd.DataFrame(result)
        #st.dataframe(df)

        df_balances = post_processing(df)
        #st.dataframe(df_balances)

        # Plot data:
        st.subheader("Market Simulator")
        chart_market_animation(df_balances, TIMESTEPS)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Gini Index")
            df_gini = gini_index(df, TIMESTEPS)
            chart_gini(df_gini)

        with col2:
            st.subheader("Trade Frequency")
            

        
        
    

    

    