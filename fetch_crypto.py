import requests
import pandas as pd

# Binance API URL for historical data
BASE_URL = "https://api.binance.com/api/v3/klines"

# Define parameters for fetching BTC/USDT daily price data
params = {
    "symbol": "BTCUSDT",  # Bitcoin to USDT
    "interval": "1d",     # Daily candles
    "limit": 1000         # Fetch last 1000 days
}

# Fetch data from Binance API
response = requests.get(BASE_URL, params=params)
data = response.json()

# Convert data to DataFrame
columns = ["timestamp", "open", "high", "low", "close", "volume", "close_time",
           "quote_asset_volume", "trades", "taker_buy_base", "taker_buy_quote", "ignore"]
df = pd.DataFrame(data, columns=columns)

# Convert timestamp to readable date
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

# Select relevant columns
df = df[["timestamp", "open", "high", "low", "close", "volume"]]

# Convert prices and volume to float
df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})

# Save to CSV file
df.to_csv("data/btc_historical_data.csv", index=False)
print("\n✅ BTC Historical Data Fetched & Saved as data/btc_historical_data.csv")

# Display first few rows
print(df.head())
