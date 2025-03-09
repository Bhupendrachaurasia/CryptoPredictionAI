from flask import Flask, render_template, jsonify
import requests
import numpy as np
import tensorflow as tf
import os

app = Flask(__name__)

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
PROXY_URL = "https://api.allorigins.win/raw?url="  # ✅ Free proxy to bypass Binance restrictions

# 📌 Function to fetch live BTC price using a proxy
def get_live_btc_price():
    try:
        proxy_request = PROXY_URL + BINANCE_URL  # ✅ Use proxy to access Binance
        headers = {"User-Agent": "Mozilla/5.0"}  # ✅ Helps avoid blocking
        response = requests.get(proxy_request, headers=headers, timeout=10)
        response.raise_for_status()  # ✅ Raise error for HTTP failures
        return float(response.json()["price"])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching BTC price via proxy: {e}")
        return None

# 📌 Function to predict next 1-minute BTC price
def predict_next_minute_price(current_price):
    model = tf.keras.models.load_model("model.h5")  # Load trained model
    scaler = np.load("scaler.npy", allow_pickle=True).item()  # Load scaler

    # Normalize the current price
    current_price_scaled = scaler.transform(np.array([[current_price]]))

    # Predict next price
    predicted_scaled = model.predict(np.array([[current_price_scaled]]))
    predicted_price = scaler.inverse_transform(predicted_scaled)[0][0]

    return float(predicted_price)  # ✅ Convert to standard Python float

# 📌 API to Get Live BTC Price
@app.route("/api/live")
def live_btc_price():
    current_price = get_live_btc_price()
    if current_price:
        return jsonify({"current_price": float(current_price)})  # ✅ Ensure it's a Python float
    return jsonify({"error": "Failed to fetch live BTC price"}), 500

# 📌 API to Get Predicted BTC Price (1 Minute Ahead)
@app.route("/api/predict")
def predict_btc_price():
    current_price = get_live_btc_price()
    if current_price:
        predicted_price = predict_next_minute_price(current_price)
        return jsonify({"predicted_price": float(predicted_price)})  # ✅ Convert to standard Python float
    return jsonify({"error": "Failed to fetch live BTC price"}), 500

# 📌 Homepage Route
@app.route("/")
def home():
    return render_template("index.html")

# 📌 Debug Route for Binance API (Helps Check API Response on Hosting)
@app.route("/debug/binance")
def debug_binance():
    try:
        proxy_request = PROXY_URL + BINANCE_URL  # ✅ Use proxy to access Binance
        headers = {"User-Agent": "Mozilla/5.0"}  # ✅ Helps avoid blocking
        response = requests.get(proxy_request, headers=headers, timeout=10)
        return jsonify(response.json())  # ✅ Return full Binance response
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500  # ✅ Show full error message

# 🚀 Run Flask App (Works for Both Local & Hosting Services)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # ✅ Railway or Render assigns a dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
