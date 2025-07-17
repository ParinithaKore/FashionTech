from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(_name_)
CORS(app)  # 🔥 Enable CORS

trends = ["Streetwear", "Minimalist", "Y2K", "Bohemian", "Athleisure"]
dates = pd.date_range(start="2020-01-01", periods=100, freq="M")
np.random.seed(42)
data = np.random.rand(len(dates), len(trends)) * 100

df = pd.DataFrame(data, columns=trends, index=dates)
df.index.name = "Date"

def simulate_trend_predictions():
    last_values = df.tail(10)
    predicted_trends = last_values.mean().to_dict()
    return {k: round(v, 2) for k, v in predicted_trends.items()}

@app.route("/predict_trends", methods=["GET"])
def predict_trends():
    predictions = simulate_trend_predictions()
    return jsonify(predictions)

if _name_ == "_main_":
    app.run(debug=True)
