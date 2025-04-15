from flask import Flask, request, send_file
import csv
import os
from datetime import datetime

app = Flask(__name__)
FAULT_LOG_FILE = "fault_log.csv"

@app.route('/log-fault', methods=['POST'])
def log_fault():
    fault_data = request.json

    # Add timestamp
    fault_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare fieldnames (headers)
    fieldnames = list(fault_data.keys())
    file_exists = os.path.exists(FAULT_LOG_FILE)

    with open(FAULT_LOG_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        writer.writerow(fault_data)

    return {'message': 'Fault logged successfully'}, 200

@app.route('/download-faults', methods=['GET'])
def download_faults():
    if not os.path.exists(FAULT_LOG_FILE):
        return "No fault log found.", 404
    return send_file(FAULT_LOG_FILE, as_attachment=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
