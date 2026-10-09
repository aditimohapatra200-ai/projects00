import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# ==========================================
# 1. STREAMLIT PAGE CONFIG & DARK THEME CSS
# ==========================================
st.set_page_config(page_title="Medical Health Assistant", layout="wide")

# Custom CSS for Dark Theme with High Visibility Inputs
st.markdown("""
    <style>
    /* Global Dark Background */
    .stApp {
        background-color: #121212;
        color: #000000;
    }
    
    /* Headers Visibility */
    h1, h2, h3, h4, h5, h6, label {
        color: #00E676 !important;
        font-weight: bold;
    }
    
    /* Input Boxes (Text, Number, Selectbox) */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 2px solid #00E676 !important;
        border-radius: 8px;
    }
    
    input {
        color: #000000 !important;
        font-weight: bold;
    }
    
    /* Buttons Styling */
    .stButton>button {
        background-color: #00E676;
        color: #FFFFFF;
        font-weight: bold;
        font-size: 18px;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #00B0FF;
        color: #FFFFFF;
    }
    
    /* Cards/Containers */
    .css-1r6slb0, .stCard {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333333;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. ML MODELS TRAINING
# ==========================================
@st.cache_resource
def train_models():
    np.random.seed(42)
    X_heart = np.column_stack([
        np.random.randint(80, 220, 200),      # BP
        np.random.randint(100, 600, 200),     # Chol
        np.random.choice([0, 1], 200),        # FBS
        np.random.choice([0, 1, 2], 200),     # RestECG
        np.random.randint(60, 220, 200),      # MaxHR
        np.random.choice([0, 1], 200),        # ExAng
        np.random.uniform(0.0, 10.0, 200),    # Oldpeak
        np.random.choice([0, 1, 2], 200),     # Slope
        np.random.choice([0, 1, 2, 3, 4], 200), # CA
        np.random.choice([0, 1, 2, 3], 200)   # Thal
    ])
    y_heart = np.random.choice([0, 1], size=200)
    scaler_heart = StandardScaler()
    X_heart_scaled = scaler_heart.fit_transform(X_heart)
    heart_model = RandomForestClassifier(n_estimators=100, random_state=42)
    heart_model.fit(X_heart_scaled, y_heart)
    X_diab = np.column_stack([
        np.random.randint(0, 18, 200),        # Pregnancies
        np.random.randint(50, 300, 200),      # Glucose
        np.random.randint(80, 220, 200),      # hba1c
        np.random.randint(0, 99, 200),        # SkinThickness
        np.random.randint(0, 840, 200),       # Insulin
        np.random.uniform(10.0, 60.0, 200),   # BMI
        np.random.uniform(0.078, 2.42, 200)  # DPF
    ])
    y_diab = np.random.choice([0, 1], size=200)
    scaler_diab = StandardScaler()
    X_diab_scaled = scaler_diab.fit_transform(X_diab)
    diab_model = SVC(probability=True, random_state=42)
    diab_model.fit(X_diab_scaled, y_diab)
    return heart_model, scaler_heart, diab_model, scaler_diab
heart_model, scaler_heart, diab_model, scaler_diab = train_models()


# ==========================================
# 3. APP HEADER
# ==========================================
st.title("🏥 Heart Disease / Diabetes Risk Predictor ")
st.markdown("-------------------------")


# ==========================================
# SECTION 1: BASIC INFORMATION
# ==========================================
st.header("👤 1. Basic Patient Information")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    name = st.text_input("Patient Name", value="John Doe")
with col_info2:
    age = st.number_input("Age", min_value=1, max_value=120, value=45)
with col_info3:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

st.markdown("---")


# ==========================================
# SECTION 2: HEART DISEASE & DIABETES PARAMETERS
# ==========================================
st.header("🩺 2. Clinical Health Parameters")

col_heart, col_diab = st.columns(2)

with col_heart:
    st.subheader("❤️ Heart Disease Parameters")
    sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Male" if x == 1 else "Female")
    cp = st.selectbox("Chest Pain Type", [1, 2, 3, 4], help="1: Typical angina, 2: Atypical angina, 3: Non-anginal pain, 4: Asymptomatic")
    bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=80, max_value=220, value=120)
    chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=100, max_value=600, value=200)
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1], format_func=lambda x: "True" if x == 1 else "False")
    restecg = st.selectbox("Resting ECG Results", [0, 1, 2], help="0: Normal, 1: ST-T wave abnormality, 2: Left ventricular hypertrophy")
    max_hr = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=150)
    exang = st.selectbox("Exercise Induced Angina", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    oldpeak = st.number_input("ST Depression (ECG)", min_value=0.0, max_value=10.0, value=1.0)
    slope = st.selectbox("Slope of Peak Exercise ST Segment", [0, 1, 2], help="0: Upsloping, 1: Flat, 2: Downsloping")
    ca = st.selectbox("Number of Major Vessels Colored by Fluoroscopy", [0, 1, 2, 3, 4])
    thal = st.selectbox("Thalassemia", [0, 1, 2, 3], help="1: Normal, 2: Fixed Defect, 3: Reversible Defect")
    rest_hr = st.number_input("Resting Heart Rate (bpm)", min_value=40, max_value=150, value=75)
    st_elev = st.number_input("ST Elevation (mm)", min_value=0.0, max_value=5.0, value=0.0)
with col_diab:
    st.subheader("🩸 Diabetes Parameters")
    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0)
    glucose = st.number_input("Fasting Glucose Level (mg/dL)", min_value=50, max_value=300, value=110)
    post_meal_glucose = st.number_input("Postprandial (2-hr) Glucose (mg/dL)", min_value=50, max_value=400, value=140)
    skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=99, value=20)
    insulin = st.number_input("Insulin Level (mu U/ml)", min_value=0, max_value=840, value=80)
    bmi = st.number_input("BMI Value (kg/m²)", min_value=10.0, max_value=60.0, value=24.5)
    hba1c = st.number_input("HbA1c Level (%)", min_value=3.5, max_value=15.0, value=5.7, step=0.1)
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.078, max_value=2.42, value=0.372, format="%.3f")
    waist_circ = st.number_input("Waist Circumference (cm)", min_value=40, max_value=200, value=85)
    hypertension = st.selectbox("History of High BP / Hypertension", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    family_history = st.selectbox("Family History of Diabetes", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    triglycerides = st.number_input("Triglycerides Level (mg/dL)", min_value=50, max_value=500, value=150)
    hdl_cholesterol = st.number_input("HDL Cholesterol (mg/dL)", min_value=20, max_value=100, value=50)
    ldl_cholesterol = st.number_input("LDL Cholesterol (mg/dL)", min_value=50, max_value=250, value=100)

st.markdown("---")

# Session State Initialization
if "submitted" not in st.session_state:
    st.session_state.submitted = False


# ==========================================
# SUBMIT & PREDICT ACTION
# ==========================================
if st.button("Submit Records & Run Prediction"):
    st.session_state.submitted = True
    
    # Machine Learning Predictions
    heart_inputs = np.array([[bp, chol, fbs, restecg, max_hr, exang, oldpeak, slope, ca, thal]])
    heart_inputs_scaled = scaler_heart.transform(heart_inputs)
    heart_risk = heart_model.predict_proba(heart_inputs_scaled)[0][1] * 100

    diab_inputs = np.array([[pregnancies, glucose, hba1c, skin_thickness, insulin, bmi, dpf]])
    diab_inputs_scaled = scaler_diab.transform(diab_inputs)
    diab_risk = diab_model.predict_proba(diab_inputs_scaled)[0][1] * 100

    st.session_state.heart_risk = round(heart_risk, 2)
    st.session_state.diab_risk = round(diab_risk, 2)


# ==========================================
# SECTION 3 & 4: PREDICTION WITH BAR CHART & FINAL OVERVIEW
# ==========================================
if st.session_state.submitted:
    
    # SECTION 3: DOCTOR'S PREDICTION WITH BAR CHART
    st.header("📊 3. Doctor Risk Prediction & Analysis")
    
    res_col1, res_col2 = st.columns([1, 1])

    with res_col1:
        st.subheader("Risk Percentage Prediction")
        st.metric(label="Heart Disease Chance", value=f"{st.session_state.heart_risk}%")
        st.metric(label="Diabetes Chance", value=f"{st.session_state.diab_risk}%")

    with res_col2:
        # Bar Chart Visualization
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#1E1E1E')
        
        categories = ['Heart Disease Risk', 'Diabetes Risk']
        risks = [st.session_state.heart_risk, st.session_state.diab_risk]
        colors = ['#FF5252', '#FFB300']
        
        bars = ax.bar(categories, risks, color=colors, width=0.4)
        ax.set_ylim(0, 100)
        ax.set_ylabel('Percentage (%)', color='white', fontsize=12)
        ax.set_title(f'Risk Comparison for {name}', color='white', fontsize=14)
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval}%", ha='center', va='bottom', color='white', fontweight='bold')

        st.pyplot(fig)

    st.markdown("---")

    # SECTION 4: DOCTOR'S FINAL OVERVIEW
    st.header("📋 4. Doctor's Final Overview & Clinical Summary")
    
    st.subheader(f"Summary Report for {name} ({age} Y/O, {gender})")
    
    # Final Condition Determination
    heart_msg = "High Risk of Heart Condition" if st.session_state.heart_risk >= 50 else "Low Risk of Heart Condition"
    diab_msg = "High Risk of Diabetes Condition" if st.session_state.diab_risk >= 50 else "Low Risk of Diabetes Condition"
    
    st.warning(f"• **Heart Assessment:** {st.session_state.heart_risk}% chance -> **{heart_msg}**")
    st.info(f"• **Diabetes Assessment:** {st.session_state.diab_risk}% chance -> **{diab_msg}**")

    # Clinical Recommendation Overview
    st.subheader("Final Medical Overview")
    final_notes = st.text_area(
        "Doctor's Final Assessment Notes:", 
        value=f"Patient {name} has been evaluated with a {st.session_state.heart_risk}% chance of Heart Disease and a {st.session_state.diab_risk}% chance of Diabetes. Primary concern lies in the parameters provided. Follow-up consultation is recommended."
    )
    
    if st.button("Save Final Medical Report"):
        patient_data = {
        'Name': [name],
        'Age': [age],
        'Gender': [gender],
        'Heart Risk': [st.session_state.heart_risk],
        'Diabetes Risk': [st.session_state.diab_risk],
        'Final Notes': [final_notes]
    }
        df = pd.DataFrame(patient_data)
        import os
        file_exists = os.path.isfile('patient_reports.csv')
        df.to_csv('patient_reports.csv', mode='a', header=not file_exists, index=False)
        st.success("Final report successfully compiled and saved!")