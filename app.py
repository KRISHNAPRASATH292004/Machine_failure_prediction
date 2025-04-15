from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import joblib
import pandas as pd
import csv
import os

app = Flask(__name__)
CORS(app)

# Load model and features
model = joblib.load("rf_model.pkl")
features = joblib.load("model_features.pkl")

# Load simulated machine data stream
machine_data_df = pd.read_csv("simulated_machine_stream.csv")
current_index = 0

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
        return jsonify({"error": str(e)}), 500

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
    fault_data = request.get_json()

    if not fault_data:
        return jsonify({"error": "No data received"}), 400

    # Define the order of features to log
    fieldnames = ["footfall", "tempMode", "AQ", "USS", "CS", "VOC", "RP", "IP", "Temperature"]
    filename = "fault_log.csv"

    # Overwrite CSV with only the latest fault row
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({key: fault_data[key] for key in fieldnames})

    return jsonify({"message": "Fault logged successfully"})

@app.route("/download-faults", methods=["GET"])
def download_faults():
    filename = "fault_log.csv"
    if not os.path.exists(filename):
        return jsonify({"error": "No faults logged yet."}), 404
    return send_file(filename, mimetype="text/csv", as_attachment=True, download_name="fault_log.csv")

if __name__ == "__main__":
    app.run(debug=True)
