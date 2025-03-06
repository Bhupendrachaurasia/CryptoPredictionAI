import pandas as pd
import numpy as np
import pandas_ta as ta
from sklearn.preprocessing import MinMaxScaler

# Load historical Bitcoin data
df = pd.read_csv("data/btc_historical_data.csv")

# Ensure proper sorting by time
df = df.sort_values(by="timestamp")

# ========================
# ADDING TECHNICAL INDICATORS
# ========================

# Moving Averages
df["SMA_10"] = ta.sma(df["close"], length=10)
df["SMA_50"] = ta.sma(df["close"], length=50)

# Relative Strength Index (RSI)
df["RSI"] = ta.rsi(df["close"], length=14)

# MACD (Moving Average Convergence Divergence)
macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
df["MACD"] = macd["MACD_12_26_9"]
df["MACD_signal"] = macd["MACDs_12_26_9"]

# Bollinger Bands
bb = ta.bbands(df["close"], length=20)
df["BB_upper"] = bb["BBU_20_2.0"]
df["BB_lower"] = bb["BBL_20_2.0"]

# NEW FEATURES TO IMPROVE TREND PREDICTIONS
df["Price_Change"] = df["close"].pct_change()  # Percentage price change
df["High_Low_Diff"] = df["high"] - df["low"]  # High-Low difference
df["Volume_Change"] = df["volume"].pct_change()  # Volume change %

# Drop NaN values created by indicators
df = df.dropna()

# ========================
# NORMALIZE DATA (Important for LSTM)
# ========================
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df[["close", "SMA_10", "SMA_50", "RSI", "MACD", "MACD_signal", "BB_upper", "BB_lower", "Price_Change", "High_Low_Diff", "Volume_Change"]])

# Save processed data
np.save("data/processed_data.npy", df_scaled)

print("✅ Data preprocessing complete! Saved as 'data/processed_data.npy'")
