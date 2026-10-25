import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="ConnectTel Churn Prediction API", version="1.0")

# Robust model path resolution
MODEL_PATH = "model/churn_pipeline.pkl"
if not os.path.exists(MODEL_PATH):
    candidate = os.path.join(os.path.dirname(__file__), "..", "model", "churn_pipeline.pkl")
    if os.path.exists(candidate):
        MODEL_PATH = candidate

# Load the frozen pipeline (preprocessor + XGBoost model) with try/except protection
model_pipeline = None
try:
    if os.path.exists(MODEL_PATH):
        model_pipeline = joblib.load(MODEL_PATH)
        print(f"INFO: Successfully loaded model pipeline from {MODEL_PATH}")
    else:
        print(f"WARNING: Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"ERROR: Failed loading model from {MODEL_PATH}: {e}")


class CustomerData(BaseModel):
    tenure: int = Field(..., ge=0, description="Months with ConnectTel")
    MonthlyCharges: float = Field(..., gt=0, description="Monthly charges in USD")
    TotalCharges: float = Field(..., ge=0, description="Total charges in USD")
    ServiceCount: int = Field(..., ge=0, le=8, description="Number of active add-on services (0-8)")
    Contract: str = Field(..., description="Contract Type: Month-to-month, One year, Two year")
    InternetService: str = Field(..., description="Internet Service: Fiber optic, DSL, No")
    PaymentMethod: str = Field(
        ...,
        description="Payment Method: Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic)",
    )
    PaperlessBilling: str = Field(..., description="Paperless Billing: Yes, No")
    Partner: str = Field(..., description="Has Partner: Yes, No")
    Dependents: str = Field(..., description="Has Dependents: Yes, No")

    class Config:
        schema_extra = {
            "example": {
                "tenure": 12,
                "MonthlyCharges": 70.35,
                "TotalCharges": 840.0,
                "ServiceCount": 3,
                "Contract": "Month-to-month",
                "InternetService": "Fiber optic",
                "PaymentMethod": "Electronic check",
                "PaperlessBilling": "Yes",
                "Partner": "No",
                "Dependents": "No",
            }
        }


@app.get("/health")
def health_check():
    return {
        "status": "200 OK",
        "message": "ConnectTel Churn API is alive",
        "model_loaded": model_pipeline is not None,
    }


@app.post("/predict")
def predict_churn(customer: CustomerData):
    if model_pipeline is None:
        raise HTTPException(status_code=500, detail="Model pipeline is not loaded on server.")

    # Pydantic v1 compatibility: use dict() instead of model_dump()
    data = customer.dict()
    # Compute the engineered feature dynamically
    data["TotalChargesPerTenure"] = data["TotalCharges"] / (data["tenure"] + 1)
    input_df = pd.DataFrame([data])
    prediction = int(model_pipeline.predict(input_df)[0])
    probability = float(model_pipeline.predict_proba(input_df)[0][1])
    return {
        "churn_prediction": "Yes" if prediction == 1 else "No",
        "churn_probability": round(probability, 4),
        "risk_level": "High Risk" if probability >= 0.5 else "Low Risk",
    }
