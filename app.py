from flask import Flask, render_template, jsonify
import requests
import numpy as np
import tensorflow as tf

app = Flask(__name__)

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# 📌 Function to fetch live BTC price
def get_live_btc_price():
    response = requests.get(BINANCE_URL)
    if response.status_code == 200:
        return float(response.json()["price"])  # Convert string to float
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

# 🚀 Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
