from pybit.unified_trading import HTTP
import get_symbols

symbol = get_symbols.get_symbols()

session = HTTP(testnet=False)

print(len(symbol))

# for i in range(len(symbol)):
    
#     try:
#         print(session.get_tickers(
#             category="spot",
#             symbol=symbol[i],
#         ))

#     except:
#         continue