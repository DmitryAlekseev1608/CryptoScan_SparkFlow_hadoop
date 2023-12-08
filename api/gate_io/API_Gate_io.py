import threading

import requests
import yaml


def get_data_from_endpoint(queue, cur_date, cur_time):
    url = "https://api.gateio.ws/api/v4/spot/currency_pairs"
    response = requests.request("GET", url)
    if response.status_code == 200:
        data = response.json()

        list_cur_date = []
        list_cur_time = []
        list_market = []
        list_symbol = []
        list_price = []

        for i in range(len(data)):
            list_cur_date.append(cur_date)
            list_cur_time.append(cur_time)
            list_market.append("gate")
            list_symbol.append(data[i]["id"])
            list_price.append(float(data[i]["buy_start"]))

        dict_market = {
            "DATA": list_cur_date,
            "TIME": list_cur_time,
            "MARKET": list_market,
            "SYMBOL": list_symbol,
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
