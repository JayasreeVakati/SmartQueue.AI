from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import sqlite3
from datetime import datetime

app = FastAPI()
model = joblib.load("model.pkl")

class InputData(BaseModel):
    hour: int
    day_of_week: int
    prev_customers: int

def log_prediction(data, prediction):
    conn = sqlite3.connect("queue_log.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            hour INTEGER,
            day_of_week INTEGER,
            prev_customers INTEGER,
            predicted_customers INTEGER
        )
    ''')
    conn.commit()
    cursor.execute('''
        INSERT INTO logs (timestamp, hour, day_of_week, prev_customers, predicted_customers)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), data.hour, data.day_of_week, data.prev_customers, prediction))
    conn.commit()
    conn.close()


@app.post("/predict")
def predict(data: InputData):
    X = [[data.hour, data.day_of_week, data.prev_customers]]
    prediction = model.predict(X)[0]
    log_prediction(data, int(prediction))
    return {"predicted_customers": int(prediction)}
