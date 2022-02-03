import streamlit as st

import numpy as np
import pandas as pd
import time
import io
from post_processing import post_processing

from visualizations import marketAnimation

# Experiment simulation configuration
from experiment import simulation


# FRONTEND / INTERFACE

# Introduction
st.title("Currency Concepts")
st.subheader("Interactive cadCAD simulation of a simple market economy.")
st.text("The model aims to demonstrate the effect of interest-bearing loans on wealth inequality")


# STREAMLIT COMPONENTS

col1, col2 = st.columns(2)
with col1:
    st.subheader("Simulation parameters:")
    n_agents = st.slider('Number of agents', 10, 200, 100)  # min: 0h, max: 23h, default: 17h
    avg_transaction_ammount = st.slider('AVG transaction ammount', 10, 100, 20)

with col2:
    st.subheader("")
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

    # Simulate
    result = simulation.run()

    df = pd.DataFrame(result)
    # st.dataframe(df)

    df = post_processing(df)
    
    # Plot data:
    marketAnimation(df)

    