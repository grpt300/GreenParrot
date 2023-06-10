import requests
import pandas as pd
import os

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

# Main function
if __name__ == '__main__':
    symbol = 'AAPL'

    fundamental_news = get_fundamental_news(symbol)
    fundamental_recommendations = get_fundamental_recommendation(symbol)
    fundamental_earnings = get_fundamental_earnings(symbol)

    print("Completed Successfully")
