import requests
import pandas as pd
import os
from sqlite_connector import create_sqlite_db, create_sqlite_table, read_sqlite_table, delete_sqlite_table, update_sqlite_table

API_KEY = os.environ.get('Strong_Fundamental_Api_Key')

# Fetch fundamental news for specific company
def get_fundamental_news(symbol):
    url = f'{os.environ.get("Strong_Fundamental_Api_Url")}company-news'
    params = {
        'symbol': symbol,
        'from': '2023-06-01',
        'to': '2023-06-10',
        'token': API_KEY
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print('Error with API request')
        return None

    return pd.DataFrame.from_dict(response.json())

# Fetch fundamental stock recommendation for specific company
def get_fundamental_recommendation(symbol):
    url = f'{os.environ.get("Strong_Fundamental_Api_Url")}stock/recommendation'
    params = {
        'symbol': symbol,
        'token': API_KEY
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print('Error with API request')
        return None

    return pd.DataFrame.from_dict(response.json())

# Fetch fundamental price target for specific company
def get_fundamental_price_target(symbol):
    url = f'{os.environ.get("Strong_Fundamental_Api_Url")}stock/price-target'
    params = {
        'symbol': symbol,
        'token': API_KEY
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print('Error with API request')
        return None

    return pd.DataFrame.from_dict(response.json())

# Fetch fundamental earnings for specific company
def get_fundamental_earnings(symbol):
    url = f'{os.environ.get("Strong_Fundamental_Api_Url")}stock/earnings'
    params = {
        'symbol': symbol,
        'token': API_KEY
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print('Error with API request')
        return None

    return pd.DataFrame.from_dict(response.json())

#Main function
def main(symbol):
    # Create SQLite database and connect using sqlalchemy
    sqlite_connection = create_sqlite_db()
    #symbol = 'ADI'

    fundamental_news = get_fundamental_news(symbol)
    fundamental_recommendations = get_fundamental_recommendation(symbol)
    fundamental_earnings = get_fundamental_earnings(symbol)

    # Create a table in SQLite database
    create_sqlite_table(sqlite_connection, 'fundamental_news', fundamental_news)
    if(fundamental_recommendations is not None):
        create_sqlite_table(sqlite_connection, 'fundamental_recommendations', fundamental_recommendations)
    if(fundamental_earnings is not None):
        create_sqlite_table(sqlite_connection, 'fundamental_earnings', fundamental_earnings)

#Main function that returns all the table details as dataframes
def get_all_data():
    # Create SQLite database and connect using sqlalchemy
    sqlite_connection = create_sqlite_db()

    fundamental_news = read_sqlite_table(sqlite_connection, 'fundamental_news')
    fundamental_recommendations = read_sqlite_table(sqlite_connection, 'fundamental_recommendations')
    fundamental_earnings = read_sqlite_table(sqlite_connection, 'fundamental_earnings')

    return fundamental_news, fundamental_recommendations, fundamental_earnings

# Main function
if __name__ == '__main__':
    # Get data from stock_list.csv to dataframe and loop through the symbols
    stock_list = pd.read_csv('stock_list.csv')
    for symbol in stock_list['Stock_Ticker']:
        try:
            main(symbol)
        except:
            print(f'Error with {symbol}')
    """
    # call get all data function
    fundamental_news, fundamental_recommendations, fundamental_earnings = get_all_data()
    print("Completed Successfully")
    """