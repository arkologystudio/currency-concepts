import streamlit as st
import pandas as pd

import matplotlib.animation as animation
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import altair as alt



def chart_balances(df, timestep):
    
    balanceArr = [agent for agent in df.iloc[timestep]]
    df = pd.DataFrame(balanceArr, columns=["Balance"])
    df['Agents'] = range(0, df.size)
    

    chart = alt.Chart(df).mark_bar().encode(
        x='Agents:O',
        y='Balance:Q'
    )
    
    st.altair_chart(chart, use_container_width=True)


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
        ax.set_ylim([0, 6000])
        return [plot]

    anim = animation.FuncAnimation(
        fig,
        animate_func,
        frames=TIMESTEPS,
        interval=60,  # in ms
    )
    
    components.html(anim.to_jshtml(), height=600)
    
    


def chart_gini(df):
    
    chart = alt.Chart(df).mark_line().encode(
        x='Timestep',
        y='Gini'
    )
    st.altair_chart(chart, use_container_width=True)