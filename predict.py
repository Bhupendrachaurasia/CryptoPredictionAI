import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import requests

# 📌 Fetch real-time BTC price
def get_live_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    if response.status_code == 200:
        return float(response.json()["price"])
    return None

# 📂 Load trained model & scaler (trained on 1 feature)
model = tf.keras.models.load_model("model.h5")
scaler = np.load("scaler.npy", allow_pickle=True).item()

# 📂 Load last 30 minutes of BTC prices from CSV
data = pd.read_csv("data/btc_minute_data.csv")
prices = data["close"].values.reshape(-1, 1)  # ✅ Fix: Use only close column

# Normalize Data
prices_scaled = scaler.transform(prices)  # ✅ Fix: Ensure only 1 feature is passed

# Prepare input for prediction (last 30 minutes)
X_input = prices_scaled[-30:].reshape(1, 30, 1)  # ✅ Fix: Ensure shape matches training

# Predict next 1-minute price
predicted_scaled = model.predict(X_input)

# Convert back to actual price scale
predicted_price = scaler.inverse_transform(predicted_scaled.reshape(-1, 1))[0][0]  # ✅ Fix: Convert correctly

# Save Prediction
np.save("predicted_prices.npy", [predicted_price])

print(f"✅ Next 1-Minute Predicted Price: ${predicted_price:.2f}")
