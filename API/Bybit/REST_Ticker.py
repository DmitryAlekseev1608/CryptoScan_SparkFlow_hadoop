import time

import requests

start_time = time.time()

url = "https://api.bybit.com/v5/market/tickers?category=spot"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
print("--- %s seconds ---" % (time.time() - start_time))
