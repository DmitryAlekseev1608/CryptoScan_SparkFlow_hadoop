from pybit.unified_trading import WebSocket
from time import sleep
import get_symbols

symbol = get_symbols.get_symbols()

ws = WebSocket(
    testnet=False,
    channel_type="spot",
)
def handle_message(message):
    print(f"{message['topic']}: {message['data']['lastPrice']}")

ws.ticker_stream(
    symbol=symbol,
    callback=handle_message
)

while True:
    sleep(1)