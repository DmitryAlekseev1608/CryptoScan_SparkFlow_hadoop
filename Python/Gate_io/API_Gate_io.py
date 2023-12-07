import requests
import threading
import config


def get_data_from_endpoint():
    url = "https://api.gateio.ws/api/v4/spot/currency_pairs"
    response = requests.request('GET', url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data from the endpoint")

def get_data_from_endpoint_infinitely(period = 1.0):
    threading.Timer(period, get_data_from_endpoint_infinitely).start()
    get_data_from_endpoint()

if __name__ == '__main__':
    get_data_from_endpoint_infinitely(period = config.period)
