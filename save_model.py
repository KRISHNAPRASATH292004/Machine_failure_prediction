import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the dataset
data = pd.read_csv("data.csv")

# Prepare features and target
X = data.drop("fail", axis=1)
y = data["fail"]

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the trained model
joblib.dump(model, 'rf_model.pkl')
joblib.dump(X.columns.tolist(), 'model_features.pkl')

print(" Model and feature list saved successfully!")
