import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Load test data and the trained model
test_data = np.load("data/test_data.npy")
scaler = np.load("models/scaler.npy", allow_pickle=True).item()  # Load the same scaler used before
model = load_model("models/bitcoin_lstm_model.h5")

# Prepare test data for prediction
time_steps = 60  # Same time window used during training
X_test, y_test = [], []
for i in range(time_steps, len(test_data)):
    X_test.append(test_data[i-time_steps:i])
    y_test.append(test_data[i, 0])

X_test, y_test = np.array(X_test), np.array(y_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], X_test.shape[2]))

# Make predictions
predictions = model.predict(X_test)

# Reverse scaling to get actual price values
predicted_prices = scaler.inverse_transform(np.hstack((predictions, np.zeros((predictions.shape[0], test_data.shape[1] - 1)))))[:, 0]
actual_prices = scaler.inverse_transform(np.hstack((y_test.reshape(-1, 1), np.zeros((y_test.shape[0], test_data.shape[1] - 1)))))[:, 0]

# Plot actual vs. predicted prices
plt.figure(figsize=(12,6))
plt.plot(actual_prices, label="Actual Prices", color="blue")
plt.plot(predicted_prices, label="Predicted Prices", color="red")
plt.xlabel("Days")
plt.ylabel("Bitcoin Price (USD)")
plt.title("Bitcoin Price Prediction - LSTM Model")
plt.legend()
plt.show()

print("\n✅ Predictions complete! Check the chart for results.")
