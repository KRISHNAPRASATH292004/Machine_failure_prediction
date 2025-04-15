from flask import Flask, jsonify, request
import joblib
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = joblib.load("rf_model.pkl")
features = joblib.load("model_features.pkl")

machine_data_df = pd.read_csv("simulated_machine_stream.csv")
current_index = 0
fault_log = []  # Store faulty rows


@app.route("/")
def home():
    return "✅ Machine Monitoring API running."


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
        return jsonify({"done": True})
    row = machine_data_df.iloc[current_index].to_dict()
    current_index += 1
    return jsonify(row)


@app.route("/log-fault", methods=["POST"])
def log_fault():
    fault = request.get_json()
    fault_log.append(fault)
    return jsonify({"status": "logged", "total": len(fault_log)})


@app.route("/download-faults", methods=["GET"])
def download_faults():
    if not fault_log:
        return jsonify({"error": "No faults logged yet."})
    df = pd.DataFrame(fault_log)
    return df.to_csv(index=False)


if __name__ == "__main__":
    app.run(debug=True)