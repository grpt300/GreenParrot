# Imports
import requests
import pandas as pd
import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

#ticker = 'FSR'
#ticker = 'TSLA'
#ticker = 'AAPL'
#ticker = 'AMZN'
#ticker = 'AMD'
ticker = 'A'

def insert_into_influx(full_list):
    token_val = os.environ.get('INFLUX_TOKEN_VALUE')
    client = influxdb_client.InfluxDBClient(url=os.environ.get('INFLUX_DB_URL'), token=token_val,
                                            org=os.environ.get('INFLUX_ORG_NAME'), verify_ssl=False)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    batch_size = 1000
    for i in range(0, len(full_list), batch_size):
        batch_data = full_list[i:i + batch_size]
        write_api.write(bucket=os.environ.get('INFLUX_BUCKET_NAME'), record=batch_data)
    client.close()

def quarterly_earnings_df(ticker):
    key = os.environ.get('Api_Key')
    base_url = "https://www.alphavantage.co/query/"
    stock = ticker
    res = requests.get(url=base_url, params={
        "function": "EARNINGS",
        "outputsize": "compact",
        "symbol": f'{stock}',
        'apikey': key})
    EPS = res.json()

    # Quarterly
    for i in range(0, len(EPS['quarterlyEarnings']) - 1):
        if i == 0:
            df = pd.DataFrame.from_dict(EPS['quarterlyEarnings'][i], orient='index')
        else:
            df_1 = pd.DataFrame.from_dict(EPS['quarterlyEarnings'][i], orient='index')
            df = pd.merge(df, df_1, left_index=True, right_index=True)
    df = df.transpose()
    df['fiscalDateEnding'] = pd.to_datetime(df['fiscalDateEnding'])
    df['reportedDate'] = pd.to_datetime(df['reportedDate'])
    df[['reported_Quarterly_EPS', 'estimated_Quarterly_EPS', 'surprise', 'surprisePercentage']] = df[
        ['reportedEPS', 'estimatedEPS', 'surprise', 'surprisePercentage']].apply(pd.to_numeric, errors='coerce')
    df = df.drop(columns=['estimatedEPS', 'reportedEPS'])
    df = df.set_index('fiscalDateEnding')
    return df

#Get single row from dataframe as parameter and use the Symbol column to get the quarterly earnings data
def get_quarterly_earnings_data(df_row):
    influx_frendly_data = lambda measurement_name, time_value, field_values, tag_values: {
        "measurement": measurement_name,
        "time": time_value,
        "fields": field_values,
        "tags": tag_values
    }
    df_data = quarterly_earnings_df(df_row['Symbol'])
    full_list = []
    for single_index, single_row in df_data.iterrows():
        #Check if the reportedDate is greater than Nov 31st 2022
        if single_row['reportedDate'] > pd.Timestamp(2022, 11, 30):
            single_data = influx_frendly_data(
                os.environ.get('Quarterly_Earnings_Table'),
                single_row['reportedDate'],
                {
                    "reported_Quarterly_EPS": single_row['reported_Quarterly_EPS'],
                    "estimated_Quarterly_EPS": single_row['estimated_Quarterly_EPS']
                },
                {
                    "symbol": df_row['Symbol']
                }
            )
            full_list.append(single_data)
    insert_into_influx(full_list)

df_input = pd.read_csv('stocks-list-all.csv')
df_input.apply(get_quarterly_earnings_data, axis=1)

#df_data = quarterly_earnings_df(ticker)
#print(df_data.columns)