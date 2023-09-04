import requests as rq
import pandas as pd
import numpy as np
import os

# Get Quaterly Earnings Data from Alpha Vantage into a Pandas Dataframe
def get_quarterly_earnings_data(symbol):
    stock = symbol
    function = "EARNINGS"
    apikey = os.environ['Api_Key']
    url = "https://www.alphavantage.co/query"
    response = rq.get(url, params={"function": function, "symbol": stock, "apikey": apikey})
    data = response.json()
    # Quarterly
    for i in range(0, len(data['quarterlyEarnings']) - 1):
        if i == 0:
            df = pd.DataFrame.from_dict(data['quarterlyEarnings'][i], orient='index')
        else:
            df_1 = pd.DataFrame.from_dict(data['quarterlyEarnings'][i], orient='index')
            df = pd.merge(df, df_1, left_index=True, right_index=True)
    df = df.transpose()
    df['fiscalDateEnding'] = pd.to_datetime(df['fiscalDateEnding'])
    df['reportedDate'] = pd.to_datetime(df['reportedDate'])
    df[['reported_Quarterly_EPS', 'estimated_Quarterly_EPS', 'surprise', 'surprisePercentage']] = df[
        ['reportedEPS', 'estimatedEPS', 'surprise', 'surprisePercentage']].apply(pd.to_numeric, errors='coerce')
    df = df.drop(columns=['estimatedEPS', 'reportedEPS'])
    df = df.set_index('fiscalDateEnding')
    return df