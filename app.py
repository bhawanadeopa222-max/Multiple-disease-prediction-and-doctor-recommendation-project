import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import urllib.parse

# Set page configuration
st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="🧑‍⚕️")

# Inject CSS for background and styles
st.markdown(
    '''<style>
    body {
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1628771065518-0d82f1938462?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-color: rgba(245, 245, 250, 0.98);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        color: #222222;
    }
    label, .stTextInput > div > label {
        color: blue !important;
        font-weight: bold;
    }
    h1, h2, h3, .stMarkdown h1 {
        color: #004466;
        font-weight: 700;
        font-size: 1.5rem;
    }
    .stAlert-success {
        background-color: green !important;
        color: #155724 !important;
        border-radius: 8px;
    }
    .stButton > button {
        background-color: white !important;
        color: black !important;
        font-weight: bold;
        border: 2px solid #007BFF !important;
        border-radius: 8px;
        padding: 0.5rem 1.25rem;
    }
    .stButton > button:hover {
        background-color: red !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #3399ff !important;
    }
    </style>''',
    unsafe_allow_html=True
)

# Load models
diabetes_model = pickle.load(open(r'C:\Users\jsdeo\OneDrive\Desktop\pbl\MINI PRO\saved_models\diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open(r'C:\Users\jsdeo\OneDrive\Desktop\pbl\MINI PRO\saved_models\rf_heart_disease_model.sav', 'rb'))
breastcancer_model = pickle.load(open(r'C:\Users\jsdeo\OneDrive\Desktop\pbl\MINI PRO\saved_models\xgboost_cancer_model.sav', 'rb'))

# Sidebar menu
with st.sidebar:
    selected = option_menu('Main Menu',
                           ['Home', 'Diabetes Prediction', 'Heart Disease Prediction', 'Breast Cancer Prediction'],
                           menu_icon='hospital-fill',
                           icons=['house', 'activity', 'heart', 'person'],
                           default_index=0)

# Homepage
if selected == 'Home':
    st.title("Welcome to Health Assistant 🧑‍⚕️")
    st.markdown("""
        This is an AI-powered health prediction system. Select a condition from the sidebar menu to begin your test. 
        We’ll also help you find doctors near you after the prediction.
    """)

# Doctor link function
def get_google_maps_url(disease, location):
    query = urllib.parse.quote(f"{disease} specialist doctors near {location}")
    return f"https://www.google.com/maps/search/{query}"

def display_doctor_link(disease_label, disease_type, location):
    maps_url = get_google_maps_url(disease_type, location)
    st.markdown(f"""
    <div style='
        border: 2px solid #007BFF;
        background-color: #e6f0ff;
        padding: 1rem;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
        margin-top: 1rem;
    '>
        🔍 <a href="{maps_url}" target="_blank" style="color: #004085; text-decoration: none;">
            Find {disease_label} Doctors Near You
        </a>
    </div>
    """, unsafe_allow_html=True)

# Diabetes Prediction
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')

    col1, col2, col3 = st.columns(3)
    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')
    with col2:
        Glucose = st.text_input('Glucose Level')
    with col3:
        BloodPressure = st.text_input('Blood Pressure value')
    with col1:
        SkinThickness = st.text_input('Skin Thickness value')
    with col2:
        Insulin = st.text_input('Insulin Level')
    with col3:
        BMI = st.text_input('BMI value')
    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
    with col2:
        Age = st.text_input('Age of the Person')

    diab_diagnosis = ''
    user_location = st.text_input("Enter your location for nearby diabetes specialists")

    if st.button('Click Here for Result'):
        try:
            user_input = [float(x) for x in [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]
            diab_prediction = diabetes_model.predict([user_input])
            diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
        except ValueError:
            diab_diagnosis = 'Please enter valid numeric inputs'

    if 'is diabetic' in diab_diagnosis.lower():
        st.markdown(f"<span style='color: red; font-weight: bold; font-size: 18px;'>{diab_diagnosis}</span>", unsafe_allow_html=True)
    elif diab_diagnosis:
        st.success(diab_diagnosis)

    if user_location:
        display_doctor_link("Diabetes", "diabetes", user_location)

# Heart Disease Prediction
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')

    inputs = [
        'Age', 'Sex (1 = male, 0 = female)', 'Chest Pain types', 'Resting Blood Pressure',
        'Serum Cholestoral in mg/dl', 'Fasting Blood Sugar > 120 mg/dl (1 = true; 0 = false)',
        'Resting Electrocardiographic results', 'Maximum Heart Rate achieved',
        'Exercise Induced Angina (1 = yes; 0 = no)', 'ST depression induced by exercise',
        'Slope of the peak exercise ST segment', 'Major vessels colored by flourosopy',
        'thal: 0 = normal; 1 = fixed defect; 2 = reversable defect']

    user_values = []
    for i in range(0, len(inputs), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(inputs):
                val = cols[j].text_input(inputs[i + j])
                user_values.append(val)

    heart_diagnosis = ''
    user_location = st.text_input("Enter your location for nearby heart specialists")

    if st.button('Click Here for Result'):
        try:
            user_input = [float(x) for x in user_values]
            heart_prediction = heart_disease_model.predict([user_input])
            heart_diagnosis = 'The person is having heart disease' if heart_prediction[0] == 1 else 'The person does not have any heart disease'
        except ValueError:
            heart_diagnosis = 'Please enter valid numeric inputs'

    if 'having' in heart_diagnosis.lower():
        st.markdown(f"<span style='color: red; font-weight: bold; font-size: 18px;'>{heart_diagnosis}</span>", unsafe_allow_html=True)
    elif heart_diagnosis:
        st.success(heart_diagnosis)

    if user_location:
        display_doctor_link("Heart", "cardiologist", user_location)

# Breast Cancer Prediction (with range hints)
if selected == "Breast Cancer Prediction":
    st.title("Breast Cancer Prediction using ML")

    fields = [
        'mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness',
        'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 'mean fractal dimension',
        'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error',
        'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error',
        'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness',
        'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension'
    ]

    field_ranges = {
        'mean radius': '6 - 28', 'mean texture': '9 - 40', 'mean perimeter': '43 - 188', 'mean area': '143 - 2501', 'mean smoothness': '0.05 - 0.16',
        'mean compactness': '0.01 - 0.35', 'mean concavity': '0.0 - 0.43', 'mean concave points': '0.0 - 0.2', 'mean symmetry': '0.1 - 0.3', 'mean fractal dimension': '0.05 - 0.1',
        'radius error': '0.1 - 3', 'texture error': '0.4 - 4', 'perimeter error': '0.8 - 22', 'area error': '6 - 550', 'smoothness error': '0.001 - 0.03',
        'compactness error': '0.002 - 0.13', 'concavity error': '0.0 - 0.4', 'concave points error': '0.0 - 0.05', 'symmetry error': '0.007 - 0.08', 'fractal dimension error': '0.001 - 0.03',
        'worst radius': '7 - 36', 'worst texture': '12 - 50', 'worst perimeter': '50 - 252', 'worst area': '185 - 4254', 'worst smoothness': '0.07 - 0.22',
        'worst compactness': '0.03 - 1.6', 'worst concavity': '0.02 - 1.2', 'worst concave points': '0.0 - 0.4', 'worst symmetry': '0.15 - 0.66', 'worst fractal dimension': '0.06 - 0.2'
    }

    breast_inputs = []
    for i in range(0, len(fields), 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j < len(fields):
                field = fields[i + j]
                val = cols[j].text_input(f"{field} (Range: {field_ranges.get(field, '')})")
                breast_inputs.append(val)

    breast_diagnosis = ''
    user_location = st.text_input("Enter your location ")

    if st.button('Click Here for Result'):
        try:
            user_input = [float(x) for x in breast_inputs]
            breast_prediction = breastcancer_model.predict([user_input])
            breast_diagnosis = "⚠️ The person has Breast Cancer" if breast_prediction[0] == 1 else "✅ The person does NOT have Breast Cancer"
        except ValueError:
            breast_diagnosis = 'Please enter valid numeric inputs'

    if 'has breast cancer' in breast_diagnosis.lower():
        st.markdown(f"<span style='color: red; font-weight: bold; font-size: 18px;'>{breast_diagnosis}</span>", unsafe_allow_html=True)
    elif breast_diagnosis:
        st.success(breast_diagnosis)

    if user_location:
        display_doctor_link("Breast Cancer", "oncologist", user_location)
