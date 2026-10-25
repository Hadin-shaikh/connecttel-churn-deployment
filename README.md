# ConnectTel Customer Churn Deployment (Capstone)

Production-grade Machine Learning deployment for ConnectTel's Customer Churn Prediction system featuring an end-to-end bundled pipeline (`StandardScaler` + `OneHotEncoder` + `XGBClassifier`), a RESTful FastAPI backend, an interactive Streamlit UI, Docker containerization, and Render cloud hosting instructions.

---

## 📂 Repository Structure

```text
connecttel-churn-deployment/
├── model/
│   └── churn_pipeline.pkl       # Serialized XGBoost pipeline (Preprocessors + XGBClassifier)
├── app/
│   └── main.py                  # FastAPI Backend (GET /health, POST /predict)
├── frontend.py                  # Streamlit UI
├── train_model.py               # Script to train & save the model artifact
├── WA_Fn-UseC_-Telco-Customer-Churn.csv # Telco churn dataset
├── Dockerfile                   # Containerization instructions
├── requirements.txt             # Dependencies
└── README.md                    # Documentation
```

---

## ⚙️ Prerequisites & Setup

### 1. Clone & Navigate
```bash
git clone <your-github-repo-url>
cd connecttel-churn-deployment
```

### 2. Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Step-by-Step Blueprint

### Step 1: Train & Generate Model Artifact (`train_model.py`)
Run the script to engineer `TotalChargesPerTenure` and `ServiceCount`, bundle the preprocessor (`StandardScaler` + `OneHotEncoder`) with `XGBClassifier`, and freeze `model/churn_pipeline.pkl`:

```bash
python train_model.py
```

*Output:*
```text
Saved model/churn_pipeline.pkl successfully!
```

---

### Step 2: Run the FastAPI Backend (`app/main.py`)
Start the inference server with Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check Endpoint:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

#### Test `GET /health` with cURL:
```bash
curl http://127.0.0.1:8000/health
```
*Response:*
```json
{
  "status": "200 OK",
  "message": "ConnectTel Churn API is alive"
}
```

#### Test `POST /predict` with cURL:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
    "tenure": 6,
    "MonthlyCharges": 85.0,
    "TotalCharges": 510.0,
    "ServiceCount": 2,
    "Contract": "Month-to-month",
    "InternetService": "Fiber optic",
    "PaymentMethod": "Electronic check",
    "PaperlessBilling": "Yes",
    "Partner": "No",
    "Dependents": "No"
  }'
```
*Response:*
```json
{
  "churn_prediction": "Yes",
  "churn_probability": 0.6847,
  "risk_level": "High Risk"
}
```

---

### Step 3: Run the Streamlit UI (`frontend.py`)
In a separate terminal window, launch the interactive user interface:

```bash
streamlit run frontend.py
```
Open your browser at `http://localhost:8501`. Enter customer account details and click **Predict Churn Risk** to view real-time probability scores and risk classification.

---

### Step 4: Docker Containerization

#### Build the Docker Image:
```bash
docker build -t connecttel-churn-app .
```

#### Run the Container:
```bash
docker run -p 8000:8000 connecttel-churn-app
```

---

### Step 5: Free Cloud Deployment on Render

1. Create a public repository on GitHub and push the project files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for ConnectTel Churn Deployment"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```
2. Log in to [Render.com](https://render.com/).
3. Click **New +** $\rightarrow$ **Web Service**.
4. Connect your GitHub repository.
5. Select **Docker** as the Runtime and choose the **Free** instance tier.
6. Render will automatically build the Docker image and provision a public URL (e.g. `https://connecttel-churn-api.onrender.com`).
7. Verify live endpoints at `https://<your-render-url>/health` and `https://<your-render-url>/docs`.

---

## 📹 Video Demo Walkthrough Checklist

For the capstone submission:
1. **API Testing**: Open Postman or your browser at `/docs`, execute a sample `POST /predict` request, and display the JSON response.
2. **Frontend UI**: Open `frontend.py` in your browser, enter customer parameters (e.g. Month-to-month contract, Fiber optic), click **Predict Churn Risk**, and demonstrate the probability gauge.

---

## 📄 License
MIT License. Developed for the End-to-End AI Project Deployment Capstone.
