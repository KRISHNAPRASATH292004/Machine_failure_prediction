from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ Enables Cross-Origin requests (needed for frontend to connect)

# Load the saved model and feature list
model = joblib.load('rf_model.pkl')
features = joblib.load('model_features.pkl')

@app.route('/')
def home():
    return "✅ Machine Fault Detection API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame([data], columns=features)
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0].tolist()

        return jsonify({
            'prediction': int(prediction),
            'probability': probability
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
