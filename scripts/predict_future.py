import numpy as np
from sklearn.linear_model import LinearRegression

# -------------------------
# YOUR DATA (EXAMPLE)
# -------------------------

# Convert dates to numbers
months = np.array([12, 1, 2]).reshape(-1, 1)

# Replace with your computed values
mean_ndvi = np.array([0.18, 0.20, 0.22])
mean_lst = np.array([30.5, 29.8, 28.9])

# -------------------------
# NDVI Prediction
# -------------------------

model_ndvi = LinearRegression()
model_ndvi.fit(months, mean_ndvi)

future_month = np.array([[3]])  # March

pred_ndvi = model_ndvi.predict(future_month)

# -------------------------
# LST Prediction
# -------------------------

model_lst = LinearRegression()
model_lst.fit(months, mean_lst)

pred_lst = model_lst.predict(future_month)

print("Predicted NDVI for March:", pred_ndvi[0])
print("Predicted LST for March (°C):", pred_lst[0])