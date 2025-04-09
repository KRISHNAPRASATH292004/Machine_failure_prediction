from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import joblib
import time

app = Flask(__name__)
CORS(app)

# Load model and features
model = joblib.load("rf_model.pkl")
features = joblib.load("model_features.pkl")

# Load data from separate CSV file
machine_data_df = pd.read_csv("simulated_machine_stream.csv")
current_index = 0


@app.route("/")
def home():
    return "✅ Machine API is running!"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame([data], columns=features)
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0].tolist()

        return jsonify({
            "prediction": int(prediction),
            "probability": probability
        })
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/live-data", methods=["GET"])
def live_data():
    global current_index
    if current_index >= len(machine_data_df):
        return jsonify({"done": True})  # Signal end of stream

    row = machine_data_df.iloc[current_index].to_dict()
    current_index += 1
    time.sleep(1)  # Simulate delay
    return jsonify(row)


if __name__ == "__main__":
    app.run(debug=True)
