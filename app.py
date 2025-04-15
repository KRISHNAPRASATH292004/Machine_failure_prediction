from flask import Flask, request, send_file
import csv
import os
from datetime import datetime

app = Flask(__name__)
FAULT_LOG_FILE = "fault_log.csv"

@app.route('/log-fault', methods=['POST'])
def log_fault():
    # Get fault data from request
    fault_data = request.json

    # Add current timestamp to the fault data
    fault_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write to CSV (appending new rows)
    file_exists = os.path.exists(FAULT_LOG_FILE)
    with open(FAULT_LOG_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(fault_data.keys()))
        
        # Write header only if the file doesn't exist
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(fault_data)

    return {'message': 'Fault logged successfully'}, 200

@app.route('/download-faults', methods=['GET'])
def download_faults():
    if not os.path.exists(FAULT_LOG_FILE):
        return "No fault log found.", 404
    return send_file(FAULT_LOG_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
