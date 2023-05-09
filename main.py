import requests
import json
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import date
import os
from sqlalchemy import create_engine
import pandas as pd
from POC.topic_extractor import perform_topic_extractor
from POC.ner_extractor import get_entities
from POC.opinion_mining import get_sentiment

def sqlite_db_connection():
    if not os.path.exists('stocks.db'):
        open('stocks.db', 'a').close()
    engine = create_engine('sqlite:///stocks.db')
    return engine

def insert_into_sqlite(df, table_name, engine):
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

def financial_strength_retreival(symbol, influx_frendly_data, api_key, function, current_date):
    url = f"{os.environ.get('Fin_Stren_Provider')}?function={function}&symbol={symbol}&apikey={api_key}"

    response = requests.get(url)
    data = json.loads(response.text)

    eps = data["EPS"]
    pe_ratio = data["PERatio"]
    roe = data["ReturnOnEquityTTM"]
    div_yield = data["DividendYield"]

    function = os.environ.get('Fin_BalSheet_Function')
    url = f"{os.environ.get('Fin_BalSheet_Provider')}?function={function}&symbol={symbol}&apikey={api_key}"

    response = requests.get(url)
    data = json.loads(response.text)



    total_liabilities = float(data["annualReports"][0]["totalLiabilities"])
    total_equity = float(data["annualReports"][0]["totalShareholderEquity"])
    debt_to_equity = total_liabilities / total_equity

    financial_strength = [
        influx_frendly_data(
            os.environ.get('Fin_Stren_Table'),
            current_date,
            {
                "EPS": eps,
                "PERatio": pe_ratio,
                "ROE": roe,
                "Divident_Yield": div_yield,
                "Dept_To_Equity": debt_to_equity
            },
            {
                "symbol": symbol
            }
        )
    ]
    sqlite_financial_strength = [{
        "date_value": current_date,
        "EPS": eps,
        "PERatio": pe_ratio,
        "ROE": roe,
        "Divident_Yield": div_yield,
        "Dept_To_Equity": debt_to_equity,
        "symbol": symbol
    }]
    return financial_strength, sqlite_financial_strength

def fundamental_analysis(symbol, current_date, influx_frendly_data):
    def merge_four_dicts(x, y, z, a):
        z.update(x)
        z.update(y)
        z.update(a)
        return z

    #Get the end time as the current date
    #Convert currentdate string to datetime object
    current_date_value = pd.to_datetime(current_date)

    end_time = current_date_value
    #Get the start time as the current date - 30 days
    start_time = (current_date_value - pd.DateOffset(days=30))
    url = os.environ.get('Fundamental_News_Provider')
    cur_date = end_time

    return_news_list = []
    while cur_date >= start_time:
        try:
            querystring = {
                "category": symbol,
                "region": "US",
                "start_time": cur_date.strftime("%Y-%m-%d"),
                "end_time": cur_date.strftime("%Y-%m-%d"),
                "size": "50"
            }
            headers = {
                "X-RapidAPI-Key": os.environ.get('Fundamental_News_Key'),
                "X-RapidAPI-Host": os.environ.get('Fundamental_News_Host')
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = json.loads(response.text)

            news_list = [
                influx_frendly_data(
                    os.environ.get('FUNDAMENTAL_NEWS_TABLE'),
                    cur_date.strftime("%Y-%m-%d"),
                    merge_four_dicts(
                        {
                            "title": news_item['title'],
                            "Source": news_item['source']
                        },
                        perform_topic_extractor([news_item['title']]),
                        get_entities(news_item['title']),
                        get_sentiment(news_item['title'])
                    ),
                    {
                        "symbol": symbol,
                        "guid": news_item['guid']
                    }
                ) for news_item in data
            ]

            sqlite_news_list = []

            return_news_list = return_news_list + news_list

            cur_date = cur_date - pd.DateOffset(days=1)
        except:
            cur_date = cur_date - pd.DateOffset(days=1)
            continue


    return return_news_list, sqlite_news_list

def technical_analysis(symbol, influx_frendly_data, api_key):
    function = os.environ.get('Technical_Analysis_Function')
    url = f"{os.environ.get('Technical_Analysis_Provider')}?function={function}&symbol={symbol}&outputsize=compact&apikey={api_key}"

    response = requests.get(url)
    data = json.loads(response.text)

    technical_data = [
        influx_frendly_data(
            os.environ.get('Technical_Analysis_Table'),
            date,
            {
                "open": data["Time Series (Daily)"][date]['1. open'],
                "high": data["Time Series (Daily)"][date]['2. high'],
                "low": data["Time Series (Daily)"][date]['3. low'],
                "close": data["Time Series (Daily)"][date]['4. close'],
                "volume": data["Time Series (Daily)"][date]['5. volume']
            },
            {
                "symbol": symbol
            }
        ) for date in data["Time Series (Daily)"]
    ]

    sqlite_technical_data = [{
        "date_value": date,
        "open": data["Time Series (Daily)"][date]['1. open'],
        "high": data["Time Series (Daily)"][date]['2. high'],
        "low": data["Time Series (Daily)"][date]['3. low'],
        "close": data["Time Series (Daily)"][date]['4. close'],
        "volume": data["Time Series (Daily)"][date]['5. volume'],
        "symbol": symbol
    } for date in data["Time Series (Daily)"]]

    return technical_data, sqlite_technical_data

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


def execute_stock(symbol):
    influx_frendly_data = lambda measurement_name, time_value, field_values, tag_values: {
        "measurement": measurement_name,
        "time": time_value,
        "fields": field_values,
        "tags": tag_values
    }
    engine = sqlite_db_connection()

    api_key = os.environ.get('Api_Key')
    function = os.environ.get('Fin_Stren_Function')
    current_date = date.today().isoformat()
    financial_strength, sqlite_financial_strength = financial_strength_retreival(symbol, influx_frendly_data, api_key, function, current_date)
    news_list, sqlite_news_list = fundamental_analysis(symbol, current_date, influx_frendly_data)
    technical_data, sqlite_technical_data = technical_analysis(symbol, influx_frendly_data, api_key)
    full_list = sum([financial_strength, news_list, technical_data[:60]], [])
    #insert_into_sqlite(pd.DataFrame.from_dict(sqlite_financial_strength), os.environ.get('Fin_Stren_Table'), engine)
    #insert_into_sqlite(pd.DataFrame.from_dict(sqlite_news_list), os.environ.get('FUNDAMENTAL_NEWS_TABLE'), engine)
    #insert_into_sqlite(pd.DataFrame.from_dict(sqlite_technical_data), os.environ.get('Technical_Analysis_Table'), engine)
    insert_into_influx(full_list)

def process_row(row):
    symbol = row['Symbol']
    execute_stock(symbol)

if __name__ == '__main__':
    #df = pd.read_csv('stocks-list.csv')
    df = pd.DataFrame.from_dict([{"Symbol": "AAPL"}])
    df.apply(process_row, axis=1)