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

# Implement Upper Trend Analysis in every week as the index is daily data as a method
def get_upper_trend(df):
    df['upper_trend'] = df['high'].rolling(5).max()
    df['upper_trend'] = df['upper_trend'].shift(1)
    df['upper_trend'] = df['upper_trend'].fillna(df['high'])
    df['upper_trend_increasing'] = df['upper_trend'] > df['upper_trend'].shift(1)
    df['upper_trend_increasing'] = df['upper_trend_increasing'].fillna(False)
    bln_upper_trend_increasing = sum(df['upper_trend_increasing']) / len(df) >= 0.8
    total_incured_percent = sum(df['upper_trend_increasing']) / len(df)
    return bln_upper_trend_increasing, total_incured_percent, df


def execute(symbol):
    bln_positive_surprise = check_positive_surprise(symbol)
    df_techanalysis_data = get_tech_analysis_data(symbol)
    # Implement Upper Trend Analysis in every week as the index is daily data
    bln_upper_trend_increasing, total_incured_percent, df_techanalysis_data = get_upper_trend(df_techanalysis_data)
    print("Symbol: " + symbol)
    print("Positive Surprise: " + str(bln_positive_surprise))
    print("Upper Trend Increasing: " + str(bln_upper_trend_increasing))
    print("Total Incured Percent: " + str(round(total_incured_percent*100)) + "%")
    print("Before 100 Days Price: " + str(df_techanalysis_data.head(1)['open'].values[0]))
    print("Now Price: " + str(df_techanalysis_data.tail(1)['open'].values[0]))
    print("successfully executed ...  ")

if __name__ == "__main__":
    df_income_data = sc.get_income_statement_data('AMZN')
    execute('AMZN')