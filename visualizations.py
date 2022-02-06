import streamlit as st


import matplotlib.animation as animation
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import plotly.express as px    
import pandas as pd


def chart_market_animation(df, TIMESTEPS):
    fig, ax = plt.subplots(1, 1)
    plot = ax.bar([agent for agent in df], df.iloc[0])
    ax.set(xlabel='Agents', ylabel='Balance (USD)',
       title='Account Balances')
    

    def animate_func(timestep):
        ax.clear()
        state = df.iloc[timestep]
        plot = ax.bar([agent for agent in df], state)
        ax.set_ylim([0, 5000])
        return [plot]

    anim = animation.FuncAnimation(
        fig,
        animate_func,
        frames=TIMESTEPS,
        interval=100,  # in ms
    )

    components.html(anim.to_jshtml(), height=600)



def chart_gini(df):
    
    st.line_chart(df, use_container_width=True)