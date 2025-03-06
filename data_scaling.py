import numpy as np

# Load predicted prices
predicted_prices = np.load("predicted_prices.npy")

# Print first 10 predictions
print(predicted_prices[:10])
