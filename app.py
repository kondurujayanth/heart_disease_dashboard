import streamlit as st
import requests
import pandas as pd
import datetime
# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="🫀Heart Disease Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Main App Background (swapped with sidebar colors) */
.stApp {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb, #89f7fe);
    color: #333333;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb, #89f7fe);
    padding: 20px;
    border-radius: 5px;
    color: #333;
}

/* Smaller section for Patient Info and Input Summary */
.small-section {
    padding: 12px !important;
    margin-bottom: 12px !important;
    font-size: 14px !important;
}

/* Button style */
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
}
.stButton>button:hover {
    background-color: #e63946;
    color: white;
}

/* Input style */
.stNumberInput>div>div>input, .stSelectbox>div>div>select {
    border-radius: 8px;
    padding: 8px;
}

/* Compact Input Summary table */
.table-container table {
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;
}
.table-container th, .table-container td {
    border: 1px solid #ddd;
    padding: 6px;
    text-align: center;
}
.table-container th {
    background-color: #f2f2f2;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar Info (swapped with main section colors)
# ----------------------------
st.sidebar.markdown("""
<p><b>ℹ️ About the App</b><br>This dashboard predicts the <b>Risk of Heart Attack</b> using a trained Machine Learning (ML) model.</p>

<p><b>Features used:</b><br>
- HighBP<br>
- HighChol<br>
- Smoker<br>
- Diabetes<br>
- PhysHlth<br>
- Sex
</p>

<p>Built with 
<b><br>FastAPI + Streamlit</b>
</p>

<p>
Developed by
<b><br>Konduru Jayanth</b></p>
</div>
""", unsafe_allow_html=True)
# ----------------------------
# App Header
# ----------------------------
st.markdown('<div style="text-align:center"><h1>🫀AI Powered Heart Disease Prediction 🤖</h1></div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:18px;">Enter patient details to predict the risk of heart disease</p>', unsafe_allow_html=True)

# ----------------------------
# Input Section
# ----------------------------
with st.container():
    st.subheader("📋 Patient Information")
    st.caption("""
    ⚙️ **Input Details:**  
    - For all dropdowns, select **0 = No** and **1 = Yes**.  
    - Adjust the Physical Health.
    """)
    col1, col2 = st.columns(2)

    with col1:
        HighBP = st.selectbox("High Blood Pressure (1=Yes, 0=No)", [0,1])
        HighChol = st.selectbox("High Cholesterol (1=Yes, 0=No)", [0,1])
        Smoker = st.selectbox("Smoker (1=Yes, 0=No)", [0,1])
        
    with col2:
        PhysHlth = st.number_input("Physical Health (0–30 days)", min_value=0, max_value=30, value=5)
        Diabetes = st.selectbox("Diabetes (0=None, 1=Type1, 2=Type2)", [0,1,2])
        Sex = st.selectbox("Sex (0=Female, 1=Male)", [0,1])

# ----------------------------
# Prediction Button with Spinner
# ----------------------------
if st.button("🔍 Predict Heart Disease Risk"):

    url = "https://heart-disease-api-xf83.onrender.com/predict"
    data = {"features": [HighBP, HighChol, Smoker, Diabetes, PhysHlth, Sex]}

    try:
        with st.spinner("Predicting heart disease risk..."):
            response = requests.post(url, json=data)
            response.raise_for_status()  # raise HTTPError for bad status
            result = response.json()

        if "prediction" in result:
            pred = result["prediction"]

            if pred == 1:
                st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, #ff7f7f, #ff4b4b);
                        color:white;
                        padding:25px;
                        border-radius:20px;
                        text-align:center;
                        font-size:24px;
                        font-weight:bold;
                        box-shadow: 0 0 20px rgba(255,0,0,0.6);
                        animation: glow 1.5s infinite alternate;
                    ">
                        🚨 <span style='font-size:30px; animation: pulse 1s infinite;'>High Risk! </span>  
                        The patient might have heart disease
                        <br><br>
                        <span style="font-size:16px;font-weight:normal; color:#fff8f0;">
                        📝 Suggestions to reduce risk:<br>
                        - Maintain a balanced diet<br>
                        - Regular exercise (30 mins/day)<br>
                        - Quit smoking & reduce alcohol<br>
                        - Regular checkups for blood pressure & cholesterol
                        </span>
                    </div>
                    <style>
                    @keyframes glow {
                        0% { box-shadow: 0 0 15px rgba(255,0,0,0.4); }
                        100% { box-shadow: 0 0 25px rgba(255,0,0,0.8); }
                    }
                    @keyframes pulse {
                        0% { transform: scale(1); }
                        50% { transform: scale(1.2); }
                        100% { transform: scale(1); }
                    }
                    </style>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, #a0f7a0, #28a745);
                        color:white;
                        padding:25px;
                        border-radius:20px;
                        text-align:center;
                        font-size:24px;
                        font-weight:bold;
                        box-shadow: 0 0 20px rgba(0,200,0,0.6);
                        animation: glow 1.5s infinite alternate;
                    ">
                        💚 <span style='font-size:28px; animation: pulse 1s infinite;'>Low Risk! </span>  
                        The patient is not likely to have heart disease
                        <br><br>
                        <span style="font-size:16px;font-weight:normal; color:#f0fff0;">
                        🎉 Tips to maintain healthy heart:<br>
                        - Continue regular exercise<br>
                        - Eat plenty of fruits & vegetables<br>
                        - Maintain a healthy weight<br>
                        - Monitor stress levels
                        </span>
                    </div>
                    <style>
                    @keyframes glow {
                        0% { box-shadow: 0 0 15px rgba(0,200,0,0.4); }
                        100% { box-shadow: 0 0 25px rgba(0,200,0,0.8); }
                    }
                    @keyframes pulse {
                        0% { transform: scale(1); }
                        50% { transform: scale(1.15); }
                        100% { transform: scale(1); }
                    }
                    </style>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No prediction received. Please try again.")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}. Try again or check your internet connection.")

# ----------------------------
# Input Summary
# ----------------------------
st.subheader("📋 Input Summary")
input_data = {
    "HighBP": [HighBP],
    "HighChol": [HighChol],
    "Smoker": [Smoker],
    "Diabetes": [Diabetes],
    "PhysHlth": [PhysHlth],
    "Sex": [Sex]
}
df_input = pd.DataFrame(input_data)

st.markdown(f"""
<div class="table-container" style="
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb, #89f7fe);
    padding: 12px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    color: #333333;
    font-family: 'Arial', sans-serif;
    font-size: 14px;
">
{df_input.to_html(index=False, escape=False)}
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Prediction timestamp, Download, and Disclaimer
# ----------------------------
prediction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"""
<p style="text-align:right; font-size:12px; color:gray;">
Last prediction timestamp: {prediction_time}
</p>
""", unsafe_allow_html=True)

st.download_button(
    label="📥 Download Input Summary as CSV",
    data=df_input.to_csv(index=False),
    file_name="heart_disease_input_summary.csv",
    mime="text/csv",
    help="Download the patient input data for your records"
)

# ----------------------------
# Footer
# ----------------------------
st.markdown("""
<hr>
<p style="text-align:center; font-size:14px;">
Made with ❤️ using <b>FastAPI + Streamlit</b> | Developed by <b>Konduru Jayanth</b>
</p>
""", unsafe_allow_html=True)


















