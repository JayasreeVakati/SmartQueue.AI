import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Dummy data generation (replace with real data if needed)
data = pd.DataFrame({
    "hour": [8, 9, 10, 11, 12, 13, 14],
    "day_of_week": [0, 0, 1, 1, 2, 2, 3],
    "prev_customers": [10, 15, 12, 18, 20, 22, 19],
    "next_customers": [12, 17, 15, 20, 22, 24, 21]
})

X = data[["hour", "day_of_week", "prev_customers"]]
y = data["next_customers"]

model = RandomForestRegressor()
model.fit(X, y)

joblib.dump(model, "model.pkl")
print("✅ Model saved as model.pkl")
