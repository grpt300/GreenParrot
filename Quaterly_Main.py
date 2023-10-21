import module.stocks_connector as sc
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# Get the quarterly earnings data for a stock in a method
def get_quarterly_earnings_data(symbol):
    df = sc.get_quarterly_earnings_data(symbol)
    return df

def get_tech_analysis_data(symbol):
    df = sc.get_technical_analysis_data(symbol)
    return df

def is_stock_increasing_trend(series):
    if(len(series) < 4):
        return False
    sub_series = series.tail(3)
    sub_series = sub_series.reset_index(drop=True)
    return (sum([series[i] <= series[i+1] for i in range(len(series)-1)])/(len(series)-1) >= 0.8) & all([sub_series[i] <= sub_series[i+1] for i in range(len(sub_series)-1)])

# Check if the stock has a positive surprise and the surprise is in increasing trend
def check_positive_surprise(symbol):
    df = get_quarterly_earnings_data(symbol)
    df = df.sort_values(by=['reportedDate'], ascending=False)
    df = df.head(6)
    df = df.sort_values(by=['reportedDate'])
    df = df.reset_index(drop=True)
    return is_stock_increasing_trend(df['surprisePercentage'])
def execute(symbol):
    bln_positive_surprise = check_positive_surprise(symbol)
    print(bln_positive_surprise)

execute('AMZN')