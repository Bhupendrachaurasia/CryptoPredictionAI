import pandas as pd
import requests
import time

# Binance API URL for historical BTC/USDT data
BINANCE_URL = "https://api.binance.com/api/v3/klines"

# Function to fetch historical BTC price data
def fetch_historical_data(symbol="BTCUSDT", interval="1d", limit=1000):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(BINANCE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        formatted_data = []

        for entry in data:
            formatted_data.append({
                "timestamp": entry[0],   # Open time
                "open": float(entry[1]), # Open price
                "high": float(entry[2]), # High price
                "low": float(entry[3]),  # Low price
                "close": float(entry[4]),# Close price
                "volume": float(entry[5])# Volume
            })

        df = pd.DataFrame(formatted_data)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")  # Convert timestamp
        return df
    else:
        print("❌ Error fetching data from Binance API")
        return None

# Fetch data and save to CSV
print("📥 Fetching BTC historical data...")
btc_data = fetch_historical_data()

if btc_data is not None:
    btc_data.to_csv("data/btc_historical_data.csv", index=False)
    print("✅ btc_historical_data.csv saved successfully!")
else:
    print("❌ Failed to save data")
