import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import requests

# 📌 Fetch 1-minute BTC price data
def fetch_minute_data():
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": "BTCUSDT", "interval": "1m", "limit": 500}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame({
            "timestamp": [entry[0] for entry in data],
            "close": [float(entry[4]) for entry in data],  # ✅ Use only close price
        })
    return None

# 📂 Load & preprocess data
data = fetch_minute_data()
if data is not None:
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
    data.to_csv("data/btc_minute_data.csv", index=False)
else:
    print("❌ Failed to fetch BTC data")

# 📌 Use only the "close" column
prices = data["close"].values.reshape(-1, 1)

# ✅ Fix: Train MinMaxScaler on only 1 feature (close price)
scaler = MinMaxScaler(feature_range=(0, 1))
prices_scaled = scaler.fit_transform(prices)

# Prepare training data
X_train, y_train = [], []
for i in range(30, len(prices_scaled)):
    X_train.append(prices_scaled[i-30:i])
    y_train.append(prices_scaled[i])

X_train, y_train = np.array(X_train), np.array(y_train)

# Build LSTM Model
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(30, 1)),  # ✅ Fix: Match input shape
    Dropout(0.2),
    LSTM(64, return_sequences=False),
    Dropout(0.2),
    Dense(32),
    Dense(1)
])
model.compile(optimizer="adam", loss="mean_squared_error")

# Train the Model
model.fit(X_train, y_train, epochs=100, batch_size=16)

# ✅ Save the Model & Scaler (now using only 1 feature)
model.save("model.h5")
np.save("scaler.npy", scaler)
print("✅ Model Training Completed & Saved!")
