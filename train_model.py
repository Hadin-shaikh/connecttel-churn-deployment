import os
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

# 1. Load & Clean Data
csv_filename = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
if not os.path.exists(csv_filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(script_dir, csv_filename)
    if os.path.exists(candidate):
        csv_filename = candidate
    elif os.path.exists(os.path.join(script_dir, "..", csv_filename)):
        csv_filename = os.path.join(script_dir, "..", csv_filename)

df = pd.read_csv(csv_filename)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].replace(" ", "0"))
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# 2. Engineer the exact features required for Project 2 as well
df["TotalChargesPerTenure"] = df["TotalCharges"] / (df["tenure"] + 1)
service_cols = [
    "PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"
]
df["ServiceCount"] = (df[service_cols] == "Yes").sum(axis=1)

# 3. Select core features for deployment
num_features = ["tenure", "MonthlyCharges", "TotalCharges", "TotalChargesPerTenure", "ServiceCount"]
cat_features = ["Contract", "InternetService", "PaymentMethod", "PaperlessBilling", "Partner", "Dependents"]

X = df[num_features + cat_features]
y = df["Churn"]

# 4. Build Preprocessor + XGBoost Pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
    ]
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, eval_metric="logloss", random_state=42)),
    ]
)

pipeline.fit(X, y)

# 5. Freeze Model + Preprocessor together
os.makedirs("model", exist_ok=True)
joblib.dump(pipeline, "model/churn_pipeline.pkl")

# Also ensure in script directory's model folder
script_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(script_dir, "model")
os.makedirs(model_dir, exist_ok=True)
joblib.dump(pipeline, os.path.join(model_dir, "churn_pipeline.pkl"))

print("Saved model/churn_pipeline.pkl successfully!")
