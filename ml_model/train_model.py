import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "dataset", "athlete_injury_dataset_100000.csv")

data = pd.read_csv(file_path)

# Encode
le_gender = LabelEncoder()
le_sport = LabelEncoder()

data["gender"] = le_gender.fit_transform(data["gender"])
data["sport"] = le_sport.fit_transform(data["sport"])

# Feature engineering (IMPORTANT)
data["workload"] = data["training_hours_per_week"] * data["fatigue_level"]
data["recovery"] = data["sleep_hours"] * data["hydration_level"]
data["risk_score"] = (
    data["workload"]
    + data["previous_injuries"] * 5
    + data["bmi"] * 0.8
    - data["recovery"]
)
def risk_label(x):
    if x < 40:
        return 0
    elif x < 100:
        return 1
    else:
        return 2

data["injury"] = data["risk_score"].apply(risk_label)

X = data.drop(["injury", "risk_score"], axis=1)
y = data["injury"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Better model
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_split=5,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Improved Accuracy:", accuracy_score(y_test, y_pred))

# Save
joblib.dump(model, "model.pkl")
joblib.dump(le_gender, "le_gender.pkl")
joblib.dump(le_sport, "le_sport.pkl")
print(data["risk_score"].describe())

print("Model Saved Successfully!")