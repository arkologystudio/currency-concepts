import streamlit as st

# Experiment simulation configuration
from models.interest_inequality.default_experiment import simulation_interest_inequality

# User interfaces
from models.interest_inequality.interface import load_interest_interface


# FRONTEND / INTERFACE

# Introduction
st.title("Currency Concepts")
st.subheader("Models: ..")
st.text("Write up about the project")



# MODEL SELECTION
model = st.selectbox("Model:", ('Interest & Inequality', '..another model'), 0, help="Choose a model to investigate")

st.text("----------------------------------------------------------------------------------")


if model == 'Interest & Inequality':
    simulation = simulation_interest_inequality
    load_interest_interface(simulation)

else:
    
    st.text("Select a simulation above.")







# if __name__ == "__main__":

    
    

    

    