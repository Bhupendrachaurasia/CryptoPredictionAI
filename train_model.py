import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# ==============================
# LOAD PREPROCESSED DATA
# ==============================
data = np.load("data/processed_data.npy")

# Define sequence length (Using 50 previous steps)
sequence_length = 50

# Prepare dataset for LSTM (Convert to sequences)
X, y = [], []
for i in range(len(data) - sequence_length):
    X.append(data[i:i+sequence_length])  # Use last 50 steps
    y.append(data[i+sequence_length, 0])  # Predict next price

X, y = np.array(X), np.array(y)

# Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# ==============================
# BUILD LSTM MODEL (IMPROVED)
# ==============================

model = Sequential([
    LSTM(256, return_sequences=True, activation="tanh", input_shape=(sequence_length, X.shape[2])),
    Dropout(0.1),
    LSTM(128, return_sequences=True, activation="tanh"),
    Dropout(0.1),
    LSTM(64, return_sequences=False, activation="tanh"),
    Dense(32, activation="relu"),
    Dense(1)  # Predict the next price
])

# Compile with lower learning rate for better accuracy
model.compile(optimizer=Adam(learning_rate=0.00005), loss="mse")

# ==============================
# TRAINING MODEL
# ==============================

print("🔄 Training LSTM model...")
history = model.fit(X_train, y_train, epochs=250, batch_size=16, validation_data=(X_test, y_test))

# Save trained model
model.save("models/lstm_model.h5")
print("✅ Model training complete! Saved as 'models/lstm_model.h5'.")

# ==============================
# GENERATE PREDICTIONS
# ==============================

# Generate predictions
predicted_prices = model.predict(X_test)

# Save predicted prices
np.save("predicted_prices.npy", predicted_prices)

print("📊 Predictions saved as 'predicted_prices.npy'.")
