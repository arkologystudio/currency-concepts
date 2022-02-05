
import numpy as np
from pandas import DataFrame

def post_processing(df):
    '''
    Refine and extract metrics from the simulation
    
    Parameters:
    df: simulation dataframe
    '''

    df = df.apply(lambda row: list(row.agents), axis=1, result_type='expand')

    return df

def gini_index(df, TIMESTEPS):

    df = df.apply(lambda row: list(row.agents), axis=1, result_type='expand') # expand agent array

    gini_arr = np.zeros(TIMESTEPS)

    for i in range(TIMESTEPS):
        sorted_arr = np.sort(df.iloc[i])
        height, area = 0, 0
        for value in sorted_arr:
            height += value
            area += height - value / 2.
        fair_area = height * len(df.iloc[i]) / 2.
        gini_arr[i] = (fair_area - area) / fair_area

    df_gini = DataFrame(gini_arr)
    return df_gini