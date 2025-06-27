import pandas_ta as ta

def add_rsi(df, period=14):
    """
    Calculates RSI and adds it to the DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame with a 'close' column.
        period (int): The time period for RSI calculation.

    Returns:
        pandas.DataFrame: The DataFrame with an 'rsi' column.
    """
    df['rsi'] = ta.rsi(df['close'], length=period)
    return df

def add_sma(df, period):
    """
    Calculates SMA and adds it to the DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame with a 'close' column.
        period (int): The time period for SMA calculation.

    Returns:
        pandas.DataFrame: The DataFrame with an f'sma_{period}' column.
    """
    df[f'sma_{period}'] = ta.sma(df['close'], length=period)
    return df

if __name__ == '__main__':
    # Example usage with dummy data
    import pandas as pd
    import numpy as np

    # Create a dummy DataFrame
    data = {'close': np.random.random(100) * 100}
    df = pd.DataFrame(data)

    # Add indicators
    df = add_rsi(df)
    df = add_sma(df, period=20)
    df = add_sma(df, period=50)

    print("DataFrame with indicators:")
    print(df.tail())
