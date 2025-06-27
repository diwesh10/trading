import pandas as pd
import pandas_ta as ta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import sys
sys.path.append(r'd:\ai new\growth_intern')


def prepare_data(df):
    """
    Prepares data for the ML model with more features.

    Args:
        df (pd.DataFrame): The input DataFrame with stock data.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: The feature set (X).
            - pd.Series: The target variable (y).
    """
    # Add features
    df['rsi'] = ta.rsi(df['close'])
    macd = ta.macd(df['close'])
    df['macd'] = macd['MACD_12_26_9']
    df['ema_10'] = ta.ema(df['close'], length=10)
    df['ema_50'] = ta.ema(df['close'], length=50)
    bb = ta.bbands(df['close'], length=20)
    df['bb_upper'] = bb['BBU_20_2.0']
    df['bb_lower'] = bb['BBL_20_2.0']
    df['returns'] = df['close'].pct_change()
    df['volume'] = df['volume']
    
    # Target: 1 if next day's return > 0.1%, else 0
    df['target'] = (df['close'].shift(-1) / df['close'] - 1 > 0.001).astype(int)
    
    # Drop rows with NaN values
    df.dropna(inplace=True)
    
    features = ['rsi', 'macd', 'ema_10', 'ema_50', 'bb_upper', 'bb_lower', 'returns', 'volume']
    X = df[features]
    y = df['target']
    
    return X, y

def train_and_predict(data):
    """
    Trains a Random Forest model and returns the prediction accuracy.

    Args:
        data (pd.DataFrame): DataFrame with stock data.

    Returns:
        float: The prediction accuracy of the model, or None if an error occurs.
    """
    if data.empty:
        return None
        
    X, y = prepare_data(data)
    
    if X.empty or y.empty:
        print("Not enough data to train the model after feature engineering.")
        return None

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

    if len(X_train) == 0 or len(X_test) == 0:
        print("Not enough data to create a train/test split.")
        return None

    # Train a Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    return accuracy

if __name__ == '__main__':
    from data.data_fetcher import fetch_daily_data
    from config import TICKERS

    for ticker in TICKERS:
        print(f"Training model for {ticker}...")
        stock_data = fetch_daily_data(ticker)
        
        if stock_data is not None and not stock_data.empty:
            accuracy = train_and_predict(stock_data)
            if accuracy is not None:
                print(f"Model accuracy for {ticker}: {accuracy:.2f}")
                print("-" * 30)
