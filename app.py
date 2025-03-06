from flask import Flask, jsonify
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# ============================
# ✅ Load Data (Safely)
# ============================

try:
    # Ensure data file exists
    if not os.path.exists("data/btc_historical_data.csv"):
        raise FileNotFoundError("btc_historical_data.csv not found!")

    print("📂 Loading historical data...")
    df = pd.read_csv("data/btc_historical_data.csv")

    # Convert timestamps to Unix format if needed
    if isinstance(df["timestamp"].iloc[0], str):  # Check if timestamps are strings (dates)
        df["timestamp"] = pd.to_datetime(df["timestamp"])  # Convert to datetime
        df["timestamp"] = df["timestamp"].astype('int64') // 10**9  # ✅ Fixed: Convert to Unix timestamps

    print("📂 Loading predicted prices...")
    if not os.path.exists("predicted_prices.npy"):
        raise FileNotFoundError("predicted_prices.npy not found! Run train_model.py to generate predictions.")

    predicted_prices = np.load("predicted_prices.npy")

    # Match timestamps with predictions
    timestamps = df["timestamp"].values[-len(predicted_prices):]

    print("✅ Data loaded successfully!")
except Exception as e:
    print("❌ Error loading data:", e)
    predicted_prices = []
    timestamps = []

# ============================
# ✅ Flask API Routes
# ============================

@app.route('/predict')
def predict():
    try:
        if len(predicted_prices) == 0:
            return jsonify({"error": "No predictions available"}), 500

        data = [{"timestamp": int(timestamps[i]), "predicted": float(predicted_prices[i][0])} for i in range(len(predicted_prices))]
        return jsonify(data)
    except Exception as e:
        print("❌ Error in /predict:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/actual')
def actual():
    try:
        actual_prices = df[["timestamp", "close"]].tail(len(predicted_prices)).to_dict(orient="records")
        return jsonify(actual_prices)
    except Exception as e:
        print("❌ Error in /actual:", e)
        return jsonify({"error": str(e)}), 500

# ============================
# ✅ Run Flask App
# ============================

if __name__ == '__main__':
    app.run(debug=True)
