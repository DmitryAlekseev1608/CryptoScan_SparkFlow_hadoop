import threading

import numpy as np
import requests
import yaml


def parsing_symbol(symbol):
    cash_4 = ["CNYX", "SNET", "USDC", "USDT"]
    cash_3 = ["BTC", "ETH", "SGD", "TRY", "USD"]

    if symbol[-4:] in cash_4:
        symbol_pars = symbol[:-5]
        cash_pars = symbol[-4:]

    elif symbol[-3:] in cash_3:
        symbol_pars = symbol[:-4]
        cash_pars = symbol[-3:]

    else:
        return np.NaN, np.NaN

    return symbol_pars, cash_pars


def get_data_from_endpoint(queue, cur_date, cur_time):
    url = "https://api.gateio.ws/api/v4/spot/tickers"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        list_cur_date = []
        list_cur_time = []
        list_market = []
        list_symbol = []
        list_cash = []
        list_price = []

        for i in range(len(data)):
            list_cur_date.append(cur_date)
            list_cur_time.append(cur_time)
            list_market.append("gate")
            symbol_pars, cash_pars = parsing_symbol(data[i]["currency_pair"])
            list_symbol.append(symbol_pars)
            list_cash.append(cash_pars)
            list_price.append(float(data[i]["last"]))

        dict_market = {
            "DATA": list_cur_date,
            "TIME": list_cur_time,
            "MARKET": list_market,
            "SYMBOL": list_symbol,
            "CASH": list_cash,
            "PRICE": list_price,
        }
        queue.put(dict_market)
        return data
    else:
        print("Failed to fetch data from the endpoint")


def get_data_from_endpoint_infinitely(period=1.0):
    threading.Timer(period, get_data_from_endpoint_infinitely).start()
    get_data_from_endpoint()


if __name__ == "__main__":
    with open("./conf/config.yaml") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    get_data_from_endpoint_infinitely(period=cfg["period"])
