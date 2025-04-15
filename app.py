from flask import Flask, request, send_file
import csv
import os

app = Flask(__name__)
FAULT_LOG_FILE = "fault_log.csv"

@app.route('/log-fault', methods=['POST'])
def log_fault():
    fault_data = request.json

    # Write headers only if the file doesn't exist
    file_exists = os.path.exists(FAULT_LOG_FILE)
    with open(FAULT_LOG_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(fault_data.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(fault_data)

    return {'message': 'Fault logged successfully'}, 200

@app.route('/download-faults', methods=['GET'])
def download_faults():
    if not os.path.exists(FAULT_LOG_FILE):
        return "No fault log found.", 404
    return send_file(FAULT_LOG_FILE, as_attachment=True)
