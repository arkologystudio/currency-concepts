import streamlit as st

import numpy as np
from pandas import DataFrame

def expand(df):
    return df.apply(lambda row: list(row.balances), axis=1, result_type='expand')
   

def gini_index(df, TIMESTEPS):

    df = df.apply(lambda row: list(row.balances), axis=1, result_type='expand') # expand agent array

    gini_arr = np.zeros(TIMESTEPS)

    for i in range(TIMESTEPS):
        sorted_arr = np.sort(df.iloc[i])
        height, area = 0, 0
        for value in sorted_arr:
            height += value
            area += height - value / 2.
        fair_area = height * (df.iloc[i]).size / 2
        gini_arr[i] = (fair_area - area) / fair_area

    df_gini = DataFrame(gini_arr, columns=["Gini"])
    return df_gini