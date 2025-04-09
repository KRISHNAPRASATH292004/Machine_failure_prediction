# Re-import required modules after environment reset
import pandas as pd
import random

# Generate 120 rows: 90 normal and 30 dangerous
def generate_stream_data(n_normal=90, n_danger=30):
    normal_rows = []
    for _ in range(n_normal):
        normal_rows.append({
            "footfall": random.randint(20, 50),
            "tempMode": random.choice([0, 1]),
            "AQ": random.randint(20, 60),
            "USS": random.randint(250, 350),
            "CS": round(random.uniform(3.5, 5.0), 2),
            "VOC": round(random.uniform(0.3, 0.5), 2),
            "RP": round(random.uniform(0.75, 0.95), 2),
            "IP": round(random.uniform(0.45, 0.65), 2),
            "Temperature": round(random.uniform(295, 310), 1)
        })

    danger_rows = []
    for _ in range(n_danger):
        danger_rows.append({
            "footfall": random.randint(5, 15),
            "tempMode": 1,
            "AQ": random.randint(85, 100),
            "USS": random.randint(430, 470),
            "CS": round(random.uniform(6.5, 7.5), 2),
            "VOC": round(random.uniform(0.9, 1.0), 2),
            "RP": round(random.uniform(1.1, 1.3), 2),
            "IP": round(random.uniform(0.85, 1.0), 2),
            "Temperature": round(random.uniform(335, 355), 1)
        })

    combined = normal_rows + danger_rows
    random.shuffle(combined)
    return combined

# Create and save the dataset
stream_data = generate_stream_data()
df_stream = pd.DataFrame(stream_data)
csv_path = csv_path = "C:/Users/krish/OneDrive/Desktop/main project/simulated_machine_stream.csv"
df_stream.to_csv(csv_path, index=False)

csv_path
