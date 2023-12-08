from pybit.unified_trading import HTTP

api_key = "YMQqRJZe7lmx786kro"
secret_key = "P70oTGhn10P3KravFvpbf2FhDE3pjnEXLfeo"

session = HTTP(
    testnet=False,
    api_key=api_key,
    api_secret=secret_key,
)

print(session.get_orderbook(category="spot", symbol="BTCUSDT"))
