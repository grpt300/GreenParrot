#Need to get the data from alfa vantage api to get the technical analysis data and implement sliding window and perason correlationto and store the date time and coefficient into another data frame

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import requests
import json
import os
from sqlalchemy import create_engine

#Get data from alfa vantage api to dataframe
def get_data(symbol, api_key):
    url = os.environ.get('Technical_Analysis_Provider')
    querystring = {
        "function": os.environ.get('Technical_Analysis_Function'),
        "symbol": symbol,
        "interval": "daily",
        "outputsize": "full",
        "apikey": api_key
    }
    response = requests.get(url, params=querystring)
    data = json.loads(response.text)
    df = pd.DataFrame(data['Time Series (Daily)']).transpose()
    df = df.sort_index()
    return df

#Get the pearson correlation coefficient
def get_pearson_correlation(df, symbol):
    correlations = []
    window_size = 365
    for i in range(len(df) - window_size + 1):
        window_start = i
        window_end = i + window_size
        window_data = df['1. open'][window_start:window_end]
        #Convert window_data to a dataframe
        window_data = pd.DataFrame(window_data)
        window_data = window_data.reset_index()

        #Convert the index column to a millisecond timestamp
        window_data['index'] = pd.to_datetime(window_data['index'])
        window_data['index'] = (window_data['index'] - window_data['index'].min()) / np.timedelta64(1, 'D')
        window_data['1. open'] = window_data['1. open'].astype(float)
        correlation = window_data['index'].corr(window_data['1. open'])
        correlations.append(correlation)
    correlation_series = pd.Series(correlations)
    correlation_series.index = df.index[window_size-1:]
    return correlation_series

#Write main function to get the data and pearson correlation coefficient
def main():
    engine = create_engine('sqlite:///./data/stock.db')
    api_key = os.environ.get('Api_Key')
    input_symbols = ['CAE.TO', 'JPM', 'TMUS', 'CRWD', 'NOW', 'CEIX', 'OSIS', 'SCI', 'VRNT', 'TNK', 'LNTH', 'DGII', 'CIVB', 'AXON']
    for symbol in input_symbols:
        try:
            df = get_data(symbol, api_key)
            correlation_series = get_pearson_correlation(df, symbol)
            correlation_series = pd.DataFrame(correlation_series)
            total_data = df.merge(correlation_series, left_index=True, right_index=True)
            total_data = total_data.reset_index()
            total_data = total_data.rename(columns={'index': 'date_value',
                                                    '1. open': 'open',
                                                    '2. high': 'high',
                                                    '3. low': 'low',
                                                    '4. close': 'close',
                                                    '5. volume': 'volume',
                                                    0: 'correlation'})
            total_data['symbol'] = symbol
            #total_data.to_csv('total_data_1year.csv')
            total_data.to_sql('total_data_1year', con=engine, if_exists='append', index=False)
            print(correlation_series)
        except Exception as e:
            print(e)
            print('failed to get data for symbol: ' + symbol)
            continue

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        print('failed to execute main')