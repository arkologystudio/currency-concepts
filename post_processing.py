


def post_processing(df):
    '''
    Refine and extract metrics from the simulation
    
    Parameters:
    df: simulation dataframe
    '''

    df = df.apply(lambda row: list(row.agents), axis=1, result_type='expand')

    return df