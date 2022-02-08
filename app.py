import streamlit as st

# Experiment simulation configuration
from models.interest_inequality.default_experiment import simulation_interest_inequality

# User interfaces
from models.interest_inequality.interface import load_interest_interface


# FRONTEND / INTERFACE

# Introduction
st.title("Currency Concepts (WIP)")
st.markdown("##### A protoype simulation environment for demonstrating key principles relevent to post-capitalist monetary design.")
st.markdown("_Developed by:_ Ross Eyre, [Arkology Studio](https://arkology.co.za)")
st.markdown("_Simulation library:_ [radCAD](https://github.com/CADLabs/radCAD) (inspired by cadCAD)")


# MODEL SELECTION
st.markdown("")
st.markdown("")
st.markdown("#### STEP 1:")
st.markdown("###### Choose a model below to get started")
st.markdown("⬇")
st.markdown("")
st.markdown("")
model = st.selectbox("Model:", ('Choose a model', 'A. Interest & Inequality', 'B. Mutual Credit'), 0)

st.text("----------------------------------------------------------------------------------")


if model == 'A. Interest & Inequality':
    simulation = simulation_interest_inequality
    load_interest_interface(simulation)
elif model == 'B. Mutual Credit':
    st.caption("Coming soon ..")
else:
    st.caption("")



    

    