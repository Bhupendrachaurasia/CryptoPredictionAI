import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# Load preprocessed data
train_data = np.load("data/train_data.npy")

# Prepare training data
time_steps = 60  # Look at the past 60 days
X_train, y_train = [], []
for i in range(time_steps, len(train_data)):
    X_train.append(train_data[i-time_steps:i])  # Use last 60 days
    y_train.append(train_data[i, 0])  # Predict closing price

X_train, y_train = np.array(X_train), np.array(y_train)

# Reshape for LSTM (samples, time steps, features)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], X_train.shape[2]))

# Build LSTM model
model = Sequential([
    LSTM(units=100, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.3),  # Prevent overfitting
    LSTM(units=100, return_sequences=False),
    Dropout(0.3),
    Dense(units=50, activation="relu"),
    Dense(units=1)  # Predict closing price
])

# Compile the model
model.compile(optimizer="adam", loss="mean_squared_error")

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32)

# Save the trained model
model.save("models/bitcoin_lstm_model.h5")
print("\n✅ Model training complete! Saved as models/bitcoin_lstm_model.h5")

# Plot training loss
plt.plot(history.history['loss'], label='Training Loss')
plt.title("LSTM Model Training Loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()
