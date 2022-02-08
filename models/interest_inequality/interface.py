"""Simulation user interace for model Interest & Inequality"""

import streamlit as st
import numpy as np
import math
import pandas as pd

from models.post_processing import expand, gini_index
from models.visualizations import chart_balances, chart_market_animation, chart_gini


def load_interest_interface(simulation):

    # MODEL DESCRIPTION
    st.header("A. Interest & Inequality")
    st.markdown("###### **A simple ABM (agent-based model) simulating a small market economy.**")
    st.markdown("The mode aims to demonstrate the effect of interest-bearing loans on wealth inequality indeces.")
    st.markdown("_Inspired by the original [Village Market Simulator](https://www.youtube.com/watch?v=04jV1zVROU8) by Will Ruddick (Grassroot Economics)_")


    with st.expander("DESCRIPTION & PURPOSE"):
        
        st.markdown("__Description:__")
        st.markdown("Within this simulated market economy, 'agents' trade goods & services with one another. Trading is fairly random resulting in a wealth distribution (Gini Index: ~30%) similar to that of Hungary, Sweden or South Korea.")  
        
        st.markdown("__Purpose:__")
        st.markdown("The model aims to demonstrate the effect of interest-bearing loans on wealth inequality indeces.")


    with st.expander("PARAMETERS & CHARTS"):
        st.markdown("__Input Parameters:__")
        st.markdown("As an analyst, you have the option to introduce interest-bearing loans to our simulated economy. When active, agents will take out loans with other agents if they cannot afford to make a desired transaction.")
        st.markdown("Feel free to play with additional parameters such as _Interest-Rate_, _Time Horizon_ & _Number of Agents_")
        
        st.markdown("__Charts:__")
        st.markdown("To give us an idea of the wealth distribution within our simulated economy the model calculates the Gini Coefficient / Index which is a statistical measure of wealth inequality between 0 - 100% (zero being the most equal)")
        st.markdown("If 'Market Simulator' is selected, an animated chart will also be rendered, showing the agents' balances over time. Feel free to cross compare the balances with the Gini Index at a given timestep to gain an intuition about their relationship.")
        
    with st.expander("THINGS TO NOTICE"):
        st.markdown("- What happens to the Gini Index when interest-bearing loans are introduced?")
        st.markdown("- With the introductions of loans, does the Gini Index continue to increase over time?")
        st.markdown("")

        
    # PARAMETER INPUTS
    st.markdown("")
    st.markdown("")
    st.markdown("#### STEP 2:")
    st.markdown("###### Set your experiment parameters")
    st.markdown("⬇")
    st.markdown("")

    st.markdown("#### Simulation parameters:")
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

    transactionChart = st.checkbox("Show market simulator", True) 
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

        st.markdown("")
        st.markdown("")
        st.markdown("#### STEP 3:")
        st.markdown("###### Analyse your results")
        st.markdown("⬇")        
        st.markdown("")
        st.markdown("")



        # PLOT RESULTS

        df = pd.DataFrame(result)
        df_balance_spread = expand(df)

        st.subheader("Agent Balances:")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("###### _Timestep:_ 0")
            chart_balances(df_balance_spread, 0)
        with col2:
            st.markdown("###### _Timestep:_ " + str(TIMESTEPS))
            chart_balances(df_balance_spread, TIMESTEPS)


        # GINI 
        st.markdown("")
        st.subheader("Gini Coefficient:")
        df_gini = gini_index(df, TIMESTEPS)        

        col1, col2 = st.columns(2)
        with col1:
            gini_start = round(df_gini.iloc[0]['Gini'], 2) 
            gini_final = round(df_gini.iloc[TIMESTEPS-1]['Gini'], 2) 
            gini_delta = round(gini_final - gini_start, 2)
            st.metric(label="Gini Index (Final)", value=(str(round(gini_final)) + " %"), delta=(str(gini_delta) + " %"))

        with col2: 
            gini_avg = round(df_gini['Gini'].mean(axis = 0))
            st.metric(label="Gini Index (AVG)", value= (str(gini_avg) + " %"))

        st.text("")
        chart_gini(df_gini)

        # Country Reference
        st.markdown("##### Comparison:")
        st.markdown("_Gini Index. [World Bank estimate (2019)](https://data.worldbank.org/indicator/SI.POV.GINI/)._")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="South Africa", value="63 %")
        col2.metric(label="Portugal", value="33 %")
        col3.metric(label="Czech Republic", value="25 %")


        # Market Simulator (animated line chart)
        if transactionChart:
            st.markdown("")
            st.subheader("Market Simulator:")
            st.text("Animated chart showing agent balances over time.")
            
            chart_market_animation(df_balance_spread, TIMESTEPS)