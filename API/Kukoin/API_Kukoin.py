import threading

import config
import requests


def get_data_from_endpoint():
    url = "https://api.kucoin.com/api/v1/market/allTickers"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["data"]["ticker"]
    else:
        print("Failed to fetch data from the endpoint")


def get_data_from_endpoint_infinitely(period=1.0):
    threading.Timer(period, get_data_from_endpoint_infinitely).start()
    get_data_from_endpoint()


if __name__ == "__main__":
    get_data_from_endpoint_infinitely(period=config.period)
