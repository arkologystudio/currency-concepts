import streamlit as st


import matplotlib.animation as animation
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import plotly.express as px    


def chart_market_animation(df, TIMESTEPS):
    #fig = plt.figure()
    fig, ax = plt.subplots(1, 1)
    plot = ax.bar([agent for agent in df], df.iloc[0])
    ax.set(xlabel='Agents', ylabel='Balance (USD)',
       title='Account Balances')
    

    def animate_func(timestep):
        
        # Sort ??
        #df_2.sort_values(by = timestep, axis=1, ascending = False)
        #df_2.sort_index(inplace=True)
        ax.clear()
        
        state = df.iloc[timestep]
        plot = ax.bar([agent for agent in df], state)
        ax.set_ylim([0, 1000])
        return [plot]

    anim = animation.FuncAnimation(
        fig,
        animate_func,
        frames=TIMESTEPS,
        interval=200,  # in ms
    )

    components.html(anim.to_jshtml(), height=600)



def chart_gini(df):

    st.line_chart(df)