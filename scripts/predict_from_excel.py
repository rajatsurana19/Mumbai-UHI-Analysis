import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# --------------------------
# LOAD EXCEL FILE
# --------------------------

file_path = r"D:/UHI-Mumbai/stats.xlsx"

df = pd.read_excel(file_path)


# --------------------------
# PREPARE TIME VARIABLE
# --------------------------

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Convert date → numeric (days since first observation)
df["t"] = (df["Date"] - df["Date"].min()).dt.days


# --------------------------
# NDVI PREDICTION
# --------------------------

X = df[["t"]]
y_ndvi = df["Mean_NDVI"]

model_ndvi = LinearRegression()
model_ndvi.fit(X, y_ndvi)


# --------------------------
# LST PREDICTION
# --------------------------

y_lst = df["Mean_LST"]

model_lst = LinearRegression()
model_lst.fit(X, y_lst)


# --------------------------
# PREDICT FUTURE DATE
# --------------------------

future_date = pd.to_datetime("2026-05-01")   # change if needed

t_future = (future_date - df["Date"].min()).days

pred_ndvi = model_ndvi.predict([[t_future]])[0]
pred_lst = model_lst.predict([[t_future]])[0]


print("Predicted NDVI:", pred_ndvi)
print("Predicted LST (°C):", pred_lst)


# --------------------------
# VISUALIZE TREND
# --------------------------

plt.scatter(df["Date"], df["Mean_LST"], label="Observed")
plt.plot(df["Date"], model_lst.predict(X), color="red", label="Trend")

plt.scatter(future_date, pred_lst, color="black", s=100, label="Prediction")

plt.title("LST Trend and Prediction")
plt.ylabel("Temperature (°C)")
plt.xlabel("Date")
plt.legend()

plt.savefig(r"D:/UHI-Mumbai/outputs/LST_prediction.png", dpi=300)
plt.show()