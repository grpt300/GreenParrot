import module.stocks_connector as sc
import pandas as pd

# Get the quarterly earnings data for a stock in a method
def get_quarterly_earnings_data(symbol):
    df = sc.get_quarterly_earnings_data(symbol)
    return df

# Execute The Method
df = get_quarterly_earnings_data('AAPL')
print(df)