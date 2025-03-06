import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load actual Bitcoin prices
df = pd.read_csv("data/btc_historical_data.csv")
actual_prices = df["close"].values

# Load predicted values (which are scaled between 0 and 1)
predicted_prices_scaled = np.load("predicted_prices.npy")

# Load the same scaler used in preprocess_data.py
scaler = MinMaxScaler()
scaler.fit(df[["close"]])  # Fit on actual prices

# Convert predictions back to real prices
predicted_prices = scaler.inverse_transform(predicted_prices_scaled)

# Adjust actual prices length to match predictions
actual_prices = actual_prices[-len(predicted_prices):]

# Plot actual vs. predicted prices
plt.figure(figsize=(12, 6))
plt.plot(actual_prices, label="Actual Prices", color="blue", linewidth=2)
plt.plot(predicted_prices, label="Predicted Prices", color="red", linestyle="dashed", linewidth=2)
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.title("📊 Actual vs. Predicted Bitcoin Prices (Denormalized)")
plt.show()
