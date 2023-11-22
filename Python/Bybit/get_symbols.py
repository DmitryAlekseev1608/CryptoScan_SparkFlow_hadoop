import requests

def get_symbols():
    
    url = "https://api.bybit.com/v5/market/tickers?category=spot"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    symbol = []

    for i in range(len(response.json()['result']['list'])):
        symbol.append(response.json()['result']['list'][i]['symbol'])
   
    return symbol