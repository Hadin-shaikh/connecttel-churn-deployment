import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Page configuration - clean title without emojis
st.set_page_config(
    page_title="TelcoChurn - Customer Churn Predictor",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inline Architectural Telecom SVGs
SIDEBAR_CITY_SVG = """
<svg viewBox="0 0 240 220" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-height: 200px; display: block; margin-top: 1.5rem;">
  <!-- City Skyline silhouettes -->
  <rect x="0" y="110" width="32" height="110" fill="#014B68" />
  <rect x="8" y="125" width="4" height="6" fill="#5CB3C1" opacity="0.6"/>
  <rect x="18" y="125" width="4" height="6" fill="#5CB3C1" opacity="0.6"/>
  <rect x="8" y="145" width="4" height="6" fill="#5CB3C1" opacity="0.6"/>
  <rect x="18" y="145" width="4" height="6" fill="#5CB3C1" opacity="0.6"/>

  <rect x="34" y="80" width="42" height="140" fill="#5CB3C1" opacity="0.9" />
  <rect x="42" y="95" width="5" height="7" fill="#FFFFFF" opacity="0.7"/>
  <rect x="54" y="95" width="5" height="7" fill="#FFFFFF" opacity="0.7"/>
  <rect x="66" y="95" width="5" height="7" fill="#FFFFFF" opacity="0.7"/>
  <rect x="42" y="115" width="5" height="7" fill="#FFFFFF" opacity="0.7"/>
  <rect x="54" y="115" width="5" height="7" fill="#FFFFFF" opacity="0.7"/>
  <rect x="66" y="115" width="5" height="7" fill="#FFFFFF" opacity="0.7"/>

  <rect x="78" y="130" width="28" height="90" fill="#013A50" />
  <rect x="85" y="145" width="4" height="6" fill="#F3BA00" opacity="0.8"/>
  <rect x="95" y="145" width="4" height="6" fill="#99D8DD" opacity="0.6"/>

  <polygon points="108,150 145,150 145,220 108,220" fill="#99D8DD" opacity="0.7" />

  <!-- Telecom Tower -->
  <path d="M 60 70 A 18 18 0 0 1 84 70" stroke="#99D8DD" stroke-width="2.5" fill="none" opacity="0.8" />
  <path d="M 54 62 A 26 26 0 0 1 90 62" stroke="#5CB3C1" stroke-width="2.5" fill="none" opacity="0.7" />
  <path d="M 48 54 A 34 34 0 0 1 96 54" stroke="#99D8DD" stroke-width="2" fill="none" opacity="0.5" />
  
  <circle cx="72" cy="74" r="5" fill="#F3BA00"/>
  <line x1="72" y1="74" x2="72" y2="105" stroke="#FFFFFF" stroke-width="3"/>
  <line x1="72" y1="105" x2="52" y2="220" stroke="#FFFFFF" stroke-width="2.5"/>
  <line x1="72" y1="105" x2="92" y2="220" stroke="#FFFFFF" stroke-width="2.5"/>
  <line x1="57" y1="135" x2="87" y2="135" stroke="#99D8DD" stroke-width="2"/>
  <line x1="57" y1="135" x2="83" y2="165" stroke="#99D8DD" stroke-width="1.8"/>
  <line x1="87" y1="135" x2="61" y2="165" stroke="#99D8DD" stroke-width="1.8"/>
  <line x1="61" y1="165" x2="83" y2="165" stroke="#99D8DD" stroke-width="2"/>
  <line x1="61" y1="165" x2="89" y2="200" stroke="#99D8DD" stroke-width="1.8"/>
  <line x1="83" y1="165" x2="55" y2="200" stroke="#99D8DD" stroke-width="1.8"/>
  <line x1="55" y1="200" x2="89" y2="200" stroke="#99D8DD" stroke-width="2"/>
</svg>
"""

RIGHT_TOWER_SVG = """
<svg viewBox="0 0 240 560" fill="none" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 240px; display: block; margin: 40px auto 0 auto;">
  <!-- Signal connection dots & lines -->
  <circle cx="20" cy="80" r="4.5" fill="#01587A" />
  <line x1="20" y1="80" x2="130" y2="15" stroke="#99D8DD" stroke-width="2" stroke-dasharray="4 4"/>
  <circle cx="130" cy="15" r="4" fill="#5CB3C1" />

  <!-- Radio Waves -->
  <path d="M 85 140 A 30 30 0 0 1 135 140" stroke="#5CB3C1" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>
  <path d="M 70 125 A 48 48 0 0 1 150 125" stroke="#99D8DD" stroke-width="2.5" fill="none" stroke-linecap="round" opacity="0.8"/>
  <path d="M 55 110 A 66 66 0 0 1 165 110" stroke="#5CB3C1" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.5"/>

  <!-- Tower Transmitter Head -->
  <circle cx="110" cy="148" r="8" fill="#01587A"/>
  <circle cx="110" cy="148" r="4" fill="#F3BA00"/>
  <line x1="110" y1="148" x2="110" y2="190" stroke="#01587A" stroke-width="3.5"/>

  <!-- Tower Legs -->
  <line x1="110" y1="190" x2="75" y2="440" stroke="#01587A" stroke-width="3.2"/>
  <line x1="110" y1="190" x2="145" y2="440" stroke="#01587A" stroke-width="3.2"/>
  <line x1="86" y1="230" x2="134" y2="230" stroke="#5CB3C1" stroke-width="2.4"/>
  <line x1="86" y1="230" x2="128" y2="280" stroke="#99D8DD" stroke-width="2"/>
  <line x1="134" y1="230" x2="92" y2="280" stroke="#99D8DD" stroke-width="2"/>
  <line x1="92" y1="280" x2="128" y2="280" stroke="#5CB3C1" stroke-width="2.4"/>
  <line x1="92" y1="280" x2="140" y2="340" stroke="#99D8DD" stroke-width="2"/>
  <line x1="128" y1="280" x2="80" y2="340" stroke="#99D8DD" stroke-width="2"/>
  <line x1="80" y1="340" x2="140" y2="340" stroke="#5CB3C1" stroke-width="2.4"/>
  <line x1="80" y1="340" x2="145" y2="410" stroke="#99D8DD" stroke-width="2"/>
  <line x1="140" y1="340" x2="75" y2="410" stroke="#99D8DD" stroke-width="2"/>
  <line x1="75" y1="410" x2="145" y2="410" stroke="#5CB3C1" stroke-width="2.4"/>

  <!-- City Skyline Behind Tower -->
  <rect x="10" y="360" width="42" height="180" fill="#99D8DD" opacity="0.6"/>
  <rect x="20" y="375" width="5" height="8" fill="#FFFFFF"/>
  <rect x="34" y="375" width="5" height="8" fill="#FFFFFF"/>
  <rect x="20" y="395" width="5" height="8" fill="#FFFFFF"/>
  <rect x="34" y="395" width="5" height="8" fill="#FFFFFF"/>

  <rect x="56" y="310" width="46" height="230" fill="#5CB3C1" opacity="0.9"/>
  <polygon points="56,310 102,290 102,540 56,540" fill="#5CB3C1"/>
  <rect x="66" y="330" width="5" height="8" fill="#FFFFFF"/>
  <rect x="80" y="330" width="5" height="8" fill="#FFFFFF"/>
  <rect x="66" y="350" width="5" height="8" fill="#FFFFFF"/>
  <rect x="80" y="350" width="5" height="8" fill="#FFFFFF"/>

  <!-- Architectural Angular Ground Blocks -->
  <polygon points="0,500 240,460 240,540 0,540" fill="#01587A"/>
  <polygon points="30,480 200,460 200,495 30,515" fill="#F3BA00"/>
</svg>
"""

# Native Theme Styling & Layout Enhancements
st.markdown(
    """
    <style>
    /* Global Page Canvas */
    .stApp {
        background-color: #F8F8FF !important;
        color: #111111;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Transparent top header bar */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Top Navigation bar */
    .top-nav {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 0.2rem 0rem 0.6rem 0rem;
    }
    .server-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #FFFFFF;
        border: 1px solid #E1E8EC;
        border-radius: 20px;
        padding: 6px 18px;
        font-size: 0.88rem;
        font-weight: 600;
        color: #111111;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .server-badge .dot-green {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #0D7D41;
        display: inline-block;
    }
    .server-badge .dot-red {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #C81E1E;
        display: inline-block;
    }

    /* Left Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #01587A !important;
        border-right: none !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }
    
    /* Modern Pill Radio Navigation in Sidebar */
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background-color: transparent !important;
        color: #E1E8EC !important;
        padding: 10px 18px !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.12) !important;
        color: #FFFFFF !important;
    }
    /* Active pill style */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background-color: #0E688B !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15) !important;
    }
    /* Hide the radio bullet circle */
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label p {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }

    /* The Main Form Card */
    div[data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E1E8EC !important;
        border-radius: 14px !important;
        box-shadow: 12px 16px 0px #246B87, 0 10px 30px rgba(1, 88, 122, 0.08) !important;
        padding: 2.2rem 2.6rem 2.2rem 2.6rem !important;
        position: relative !important;
    }

    /* Card Header Container with Non-overlapping Vertical Yellow Accent */
    .card-header-flex {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        margin-bottom: 1.6rem;
    }
    .header-accent-bar {
        width: 5px;
        height: 48px;
        background-color: #F3BA00;
        border-radius: 3px;
        flex-shrink: 0;
        margin-top: 3px;
    }

    /* Card Header Typography */
    .section-label {
        color: #01587A;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .main-title {
        color: #01587A;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0 0 6px 0;
        line-height: 1.2;
    }
    .main-subtitle {
        color: #6B7280;
        font-size: 0.98rem;
    }

    /* Input Fields: Crisp White Background & 1px Grey Border */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E1E8EC !important;
        border-radius: 6px !important;
        box-shadow: none !important;
    }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {
        border-color: #01587A !important;
        box-shadow: 0 0 0 1px #01587A !important;
    }
    div[data-baseweb="input"] input {
        color: #111111 !important;
        background-color: #FFFFFF !important;
        font-weight: 500 !important;
    }
    label[data-testid="stWidgetLabel"] p {
        color: #01587A !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 4px !important;
    }

    /* Primary Predict Button - Solid Deep Teal */
    div[data-testid="stFormSubmitButton"] > button,
    div.stButton > button,
    button[kind="secondaryFormSubmit"],
    button[kind="primaryFormSubmit"] {
        background-color: #01587A !important;
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.72rem 2rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 5px rgba(1, 88, 122, 0.25) !important;
    }
    div[data-testid="stFormSubmitButton"] > button p,
    button[kind="secondaryFormSubmit"] p,
    button[kind="primaryFormSubmit"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover,
    button[kind="secondaryFormSubmit"]:hover,
    button[kind="primaryFormSubmit"]:hover {
        background-color: #01435D !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 10px rgba(1, 88, 122, 0.35) !important;
    }

    /* Results Card */
    .result-box-high {
        background-color: #FFFFFF;
        border: 1px solid #E1E8EC;
        border-left: 6px solid #C81E1E;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-top: 1.6rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .result-box-low {
        background-color: #FFFFFF;
        border: 1px solid #E1E8EC;
        border-left: 6px solid #0D7D41;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-top: 1.6rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def check_backend():
    try:
        r = requests.get(f"{API_URL}/health", timeout=2)
        if r.status_code == 200:
            return True
    except Exception:
        pass
    return False


is_online = check_backend()

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 2.2rem; margin-top: 0.5rem;">
          <svg width="28" height="24" viewBox="0 0 24 20" fill="none">
            <rect x="2" y="10" width="4" height="10" rx="1.5" fill="#F3BA00"/>
            <rect x="9" y="5" width="4" height="15" rx="1.5" fill="#F3BA00"/>
            <rect x="16" y="0" width="4" height="20" rx="1.5" fill="#F3BA00"/>
          </svg>
          <span style="font-size: 1.42rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.3px;">TelcoChurn</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_choice = st.radio(
        "Navigation Menu",
        options=["Predictor", "About"],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    # Architectural cityscape SVG at bottom of sidebar
    st.markdown(SIDEBAR_CITY_SVG, unsafe_allow_html=True)
    st.caption("<center style='color: #99D8DD; font-size: 0.75rem; letter-spacing: 0.5px;'>ConnectTel Infrastructure v1.0</center>", unsafe_allow_html=True)


# ----------------- TOP BAR (Clean & Minimal, No Duplicate Branding) -----------------
if is_online:
    badge_html = """
    <div class="top-nav">
      <div class="server-badge">
        <span class="dot-green"></span>
        <span>Server Online</span>
      </div>
    </div>
    """
else:
    badge_html = """
    <div class="top-nav">
      <div class="server-badge">
        <span class="dot-red"></span>
        <span>Server Offline</span>
      </div>
    </div>
    """
st.markdown(badge_html, unsafe_allow_html=True)


# ----------------- MAIN VIEW: PREDICTOR -----------------
if nav_choice == "Predictor":
    # 2-Column Layout: Left is the white elevated prediction card, Right is the transmission tower illustration
    content_col, illust_col = st.columns([4.2, 1.4], gap="large")

    with content_col:
        with st.form("churn_prediction_form"):
            # Header inside the elevated white card with clean non-overlapping accent
            st.markdown(
                """
                <div class="card-header-flex">
                  <div class="header-accent-bar"></div>
                  <div>
                    <div class="section-label">CUSTOMER ANALYTICS</div>
                    <div class="main-title">Customer Churn Predictor</div>
                    <div class="main-subtitle">Enter the customer details below to predict the likelihood of churn.</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col_left, col_right = st.columns(2, gap="large")

            with col_left:
                tenure = st.number_input(
                    "Tenure (Months)",
                    min_value=0,
                    max_value=100,
                    value=6,
                    step=1,
                    help="Months customer has stayed with company",
                )
                monthly_charges = st.number_input(
                    "Monthly Charges ($)",
                    min_value=10.0,
                    max_value=250.0,
                    value=85.00,
                    step=0.5,
                    format="%.2f",
                )
                total_charges = st.number_input(
                    "Total Charges ($)",
                    min_value=0.0,
                    max_value=15000.0,
                    value=510.00,
                    step=1.0,
                    format="%.2f",
                )
                service_count = st.slider(
                    "Number of Add-on Services",
                    min_value=0,
                    max_value=8,
                    value=2,
                    help="Active services (Streaming, Security, Backup, Tech Support, etc.)",
                )
                contract = st.selectbox(
                    "Contract Type",
                    options=["Month-to-month", "One year", "Two year"],
                    index=0,
                )

            with col_right:
                internet = st.selectbox(
                    "Internet Service",
                    options=["Fiber optic", "DSL", "No"],
                    index=0,
                )
                payment = st.selectbox(
                    "Payment Method",
                    options=[
                        "Electronic check",
                        "Mailed check",
                        "Bank transfer (automatic)",
                        "Credit card (automatic)",
                    ],
                    index=0,
                )
                paperless = st.selectbox(
                    "Paperless Billing",
                    options=["Yes", "No"],
                    index=0,
                )
                partner = st.selectbox(
                    "Has Partner?",
                    options=["No", "Yes"],
                    index=0,
                )
                dependents = st.selectbox(
                    "Has Dependents?",
                    options=["No", "Yes"],
                    index=0,
                )

            st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
            predict_btn = st.form_submit_button("Predict Churn Risk  →")

        if predict_btn:
            payload = {
                "tenure": int(tenure),
                "MonthlyCharges": float(monthly_charges),
                "TotalCharges": float(total_charges),
                "ServiceCount": int(service_count),
                "Contract": contract,
                "InternetService": internet,
                "PaymentMethod": payment,
                "PaperlessBilling": paperless,
                "Partner": partner,
                "Dependents": dependents,
            }

            try:
                resp = requests.post(f"{API_URL}/predict", json=payload, timeout=8)
                if resp.status_code == 200:
                    data = resp.json()
                    prob = data["churn_probability"]
                    prediction = data["churn_prediction"]
                    risk = data["risk_level"]

                    if prediction == "Yes":
                        st.markdown(
                            f"""
                            <div class="result-box-high">
                              <div style="font-size: 1.15rem; font-weight: 700; color: #C81E1E;">
                                High Churn Risk Detected — Probability: {prob * 100:.1f}%
                              </div>
                              <p style="margin: 0.5rem 0 0 0; color: #374151; font-size: 0.94rem; line-height: 1.5;">
                                <strong>Recommendation:</strong> Account at elevated risk. Proactively offer a long-term contract discount, bundled streaming services, or automated billing incentives.
                              </p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="result-box-low">
                              <div style="font-size: 1.15rem; font-weight: 700; color: #0D7D41;">
                                Customer Likely to Retain — Churn Probability: {prob * 100:.1f}%
                              </div>
                              <p style="margin: 0.5rem 0 0 0; color: #374151; font-size: 0.94rem; line-height: 1.5;">
                                <strong>Recommendation:</strong> Customer health score is strong. Maintain standard satisfaction touchpoints and routine loyalty perks.
                              </p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.error(f"API Service Error ({resp.status_code}): {resp.text}")
            except Exception as ex:
                st.markdown(
                    f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #E1E8EC; border-left: 5px solid #01587A; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                      <div style="font-weight: 700; color: #01587A;">Unable to connect to the prediction service</div>
                      <div style="color: #6B7280; font-size: 0.9rem; margin-top: 4px;">
                        Check that the FastAPI server is running and accessible at <code>{API_URL}</code>.
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with illust_col:
        # Architectural transmission tower on the right
        st.markdown(RIGHT_TOWER_SVG, unsafe_allow_html=True)


# ----------------- MAIN VIEW: ABOUT (Formal & Humanized Narrative) -----------------
elif nav_choice == "About":
    st.markdown(
        """
        <div style="background-color: #FFFFFF; border: 1px solid #E1E8EC; border-radius: 14px; box-shadow: 12px 16px 0px #246B87, 0 10px 30px rgba(1, 88, 122, 0.08); padding: 2.4rem 2.8rem; max-width: 960px;">
          <div class="card-header-flex">
            <div class="header-accent-bar"></div>
            <div>
              <div class="section-label">SYSTEM ARCHITECTURE</div>
              <div class="main-title">About TelcoChurn</div>
              <div class="main-subtitle">ConnectTel Enterprise Customer Churn Analytics Platform</div>
            </div>
          </div>
          
          <p style="color: #374151; font-size: 1rem; line-height: 1.75; margin-bottom: 1.25rem;">
            TelcoChurn is a predictive analytics tool designed to help customer success teams identify at-risk accounts before they churn. By leveraging an ensemble XGBoost model trained on historical customer accounts, the platform evaluates behavioral signals, contract commitments, and service portfolios to forecast churn probabilities in real time.
          </p>

          <p style="color: #374151; font-size: 1rem; line-height: 1.75; margin-bottom: 1.25rem;">
            Every customer record is processed through an automated feature engineering pipeline that computes tenure-charge ratios, standardizes financial metrics, and one-hot encodes account categories. This unified data architecture enables retention specialists to pinpoint key churn indicators early and proactively deploy targeted offers, such as annual contract discounts or bundled service incentives.
          </p>

          <p style="color: #374151; font-size: 1rem; line-height: 1.75; margin-bottom: 1.25rem;">
            The application is packaged as a containerized, cloud-ready service that couples a high-throughput FastAPI inference engine with this streamlined analytical dashboard. Interactive OpenAPI documentation, automated health monitoring, and schema validation endpoints are accessible directly via the backend service at <a href="http://127.0.0.1:8000/docs" target="_blank" style="color: #01587A; font-weight: 600; text-decoration: underline;">/docs</a>.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
