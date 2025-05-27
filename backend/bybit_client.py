import os
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

load_dotenv()

API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")

client = HTTP(api_key=API_KEY, api_secret=API_SECRET, testnet=True)

def get_balance():
    return client.get_wallet_balance(accountType="UNIFIED")

def place_market_order(symbol: str, amount: float, market_unit: str):
    return client.place_order(
        category="spot",
        symbol=symbol,
        side="Buy",
        orderType="Market",
        qty=str(amount),
        marketUnit=market_unit
    )

def get_pnl(symbol: str):
    return client.get_closed_pnl(category="linear", symbol=symbol)
