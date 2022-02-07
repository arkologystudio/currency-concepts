import streamlit as st
import pandas as pd

import matplotlib.animation as animation
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import plotly.express as px    
import altair as alt





def chart_market_animation(df, TIMESTEPS):

    pct_complete = 0
    my_bar = st.progress(pct_complete)
    

    fig, ax = plt.subplots(1, 1)
    plot = ax.bar([agent for agent in df], df.iloc[0])
    ax.set(xlabel='Agents', ylabel='Balance (USD)',
       title='Account Balances')
    

    def animate_func(timestep):

        my_bar.progress(timestep/TIMESTEPS)

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
    
    #st.line_chart(df, use_container_width=True)
    chart = alt.Chart(df).mark_line().encode(
        x='Timestep',
        y='Gini'
    )
    st.altair_chart(chart, use_container_width=True)