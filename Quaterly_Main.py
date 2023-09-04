import module.stocks_connector as sc
import pandas as pd

# Get the quarterly earnings data for a stock in a method
def get_quarterly_earnings_data(symbol):
    df = sc.get_quarterly_earnings_data(symbol)
    return df

def get_tech_analysis_data(symbol):
    df = sc.get_technical_analysis_data(symbol)
    return df

# Check if the stock has a positive surprise and the surprise is in increasing trend
def check_positive_surprise(symbol):
    df = get_quarterly_earnings_data(symbol)
    df = df.sort_values(by=['reportedDate'], ascending=False)
    df = df.head(6)
    df = df.reset_index(drop=True)
    df['diff'] = df['surprisePercentage'].diff()
    df['diff'].fillna(0.1, inplace=True)
    df['is_greater'] = df['diff'] > 0
    if(df[df['is_greater'] == False].shape[0] > 0):
        return False
    else:
        return True
def execute(symbol):
    bln_positive_surprise = check_positive_surprise(symbol)

execute('AAPL')