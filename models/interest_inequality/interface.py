"""Simulation user interace for model Interest & Inequality"""

import streamlit as st
import numpy as np
import math
import pandas as pd

from models.post_processing import expand, gini_index
from models.visualizations import chart_market_animation, chart_gini


def load_interest_interface(simulation):

    # MODEL DESCRIPTION
    st.header("Interest & Inequality")
    st.text("Agent-based radCAD/cadCAD simulation of a simple market economy.")
    st.text("The model aims to demonstrate the effect of interest-bearing loans")
    st.text("on wealth inequality indeces.")


    # PARAMETER INPUTS
    st.subheader("Simulation parameters:")
    col1, col2, col3 = st.columns(3)
    with col1:

        option = st.selectbox("Loans:", ('Inactive', 'Active'), 0, help="If active, agents will take out loans with one another if they cannot afford to make a transaction.")
        loans_active = False # default
        if option == 'Active': 
            print("Loans Activated")
            loans_active = True

        interest_rate = st.slider("Interets Rate (%):", 1.0, 15.0, 5.0, 1.0) / 100

    with col2:
        st.subheader("")
        
    with col3:
        n_agents = st.slider('Number of agents', 10, 100, 50, 10)  # params: min, max, default, step
        TIMESTEPS = st.slider("Time Horizon (Days): ", 50, 1000, 200, 50)  

    st.text("----------------------------------------------------------------------------------")

    transactionChart = st.checkbox("Show market simulator") 
    simulate = st.button("Simulate")


    # SIMULATE
    if simulate:

        # Update Simulation Parameters based on user input
        simulation.model.params.update({
            "n_agents": [n_agents], 
            "loans_active": [loans_active],
            "interest_rate": [interest_rate]
        })

        simulation.model.initial_state.update({
            #"balances": np.full(n_agents, 500,  dtype=int)
            "balances": np.random.randint(100, 2000, n_agents), # randomize starting balances

        })

        # RUN SIMULATION
        simulation.timesteps = TIMESTEPS
        st.write("Running simulation ..")
        result = simulation.run()
        st.text("----------------------------------------------------------------------------------")


        df = pd.DataFrame(result)
        

        # DATA POST-PROCESSING
        #st.subheader("Balances - DataFrame")
        df_balance_spread = expand(df)
        #st.dataframe(df_balance_spread)


        # PLOT RESULTS

        # Gini index (line chart)
        st.subheader("Gini Coefficient:")
        df_gini = gini_index(df, TIMESTEPS)        

        col1, col2 = st.columns(2)
        with col1:
            gini_start = round(df_gini.iloc[0]['Gini'], 2) 
            gini_final = round(df_gini.iloc[TIMESTEPS-1]['Gini'], 2) 
            gini_delta = round(gini_final - gini_start, 2)
            st.metric(label="Gini Index (Final)", value=(str(round(gini_final)) + " %"), delta=(str(gini_delta) + " %"))

        with col2: 
            gini_avg = round(df_gini['Gini'].mean(axis = 0), 2)
            st.metric(label="Gini Index (AVG)", value= (str(gini_avg) + " %"))

        st.text("")
        chart_gini(df_gini)

        # Country Reference
        st.subheader("Comparison:")
        st.text("Gini Index. World Bank estimate (2019).")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="South Africa", value="63 %")
        col2.metric(label="Portugal", value="33 %")
        col3.metric(label="Czech Republic", value="25 %")


        # Market Simulator (animated line chart)
        if transactionChart:
            st.subheader("Market Simulator:")
            st.text("Animated chart showing agent transactions over time.")
            chart_market_animation(df_balance_spread, TIMESTEPS)