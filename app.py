import streamlit as st
import requests
import pandas as pd
import datetime

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="🫀Heart Attack Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Custom CSS Styling
# ----------------------------
st.markdown("""
<style>
/* App background gradient */
.stApp {
    background: linear-gradient(120deg, #ffe6e6, #fcfcfc);
    color: #333;
    font-family: 'Arial', sans-serif;
}

/* Section cards */
.section {
    background-color: white;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}

/* Sidebar */
.stSidebar .css-1d391kg { 
    background: linear-gradient(135deg, #ffd6d6, #ffc0b3);
    border-radius: 15px;
    padding: 20px;
    color: #333;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}

/* Button */
.stButton>button {
    background: linear-gradient(135deg, #ff7f7f, #ff4b4b);
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 25px;
    transition: transform 0.2s;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* Inputs */
.stNumberInput>div>div>input, .stSelectbox>div>div>select {
    border-radius: 8px;
    padding: 8px;
}

/* Table */
.table-container table {
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.table-container th, .table-container td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
}
.table-container th {
    background-color: #f0c2c2;
    color: #333;
}
.table-container tr:nth-child(even) {
    background-color: #f9f9f9;
}

/* Risk Cards */
.risk-card {
    border-radius: 15px;
    padding: 20px;
    color: white;
    font-weight: bold;
    font-size: 22px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar Info
# ----------------------------
st.sidebar.markdown("""
<div>
<p><b>About</b><br>This dashboard predicts the <b>risk of Heart Attack</b> using a trained ML model.</p>

<p><b>Features used:</b><br>
- HighBP, HighChol<br>
- Smoker, Diabetes<br>
- PhysHlth, Sex
</p>

<p>Built with <b>FastAPI + Streamlit</b></p>

<p>Developed by <b>Konduru Jayanth</b></p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# App Header
# ----------------------------
st.markdown('<div style="text-align:center; color:#b22222;"><h1>🫀 Heart Attack Predictor</h1></div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:18px;">Enter patient details to predict heart disease risk</p>', unsafe_allow_html=True)

# ----------------------------
# Input Section
# ----------------------------
with st.container():
    st.subheader("📋 Patient Information")
    st.caption("⚙️ **Input Details:** 0 = No, 1 = Yes. Physical Health: 0–30 days")
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
# Prediction Button
# ----------------------------
if st.button("🔍 Predict Heart Disease Risk"):
    url = "https://heart-disease-api-xf83.onrender.com/predict"
    data = {"features": [HighBP, HighChol, Smoker, Diabetes, PhysHlth, Sex]}

    try:
        with st.spinner("Predicting..."):
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()

        if "prediction" in result:
            pred = result["prediction"]

            if pred == 1:
                st.markdown(f"""
                    <div class='risk-card' style='background: linear-gradient(135deg, #ff9999, #ff4d4d);'>
                        🚨 High Risk! Potential heart disease detected
                        <br><span style="font-size:15px;font-weight:normal;">📝 Suggestions:<br>- Balanced diet<br>- Exercise<br>- Quit smoking<br>- Regular checkups</span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class='risk-card' style='background: linear-gradient(135deg, #b9fbc0, #4cd137);'>
                        💚 Low Risk! Heart health looks good
                        <br><span style="font-size:15px;font-weight:normal;">🎉 Tips:<br>- Continue exercise<br>- Eat fruits & vegetables<br>- Maintain healthy weight<br>- Monitor stress</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No prediction received. Try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")

# ----------------------------
# Input Summary Table
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
st.markdown(f"<div class='table-container'>{df_input.to_html(index=False, escape=False)}</div>", unsafe_allow_html=True)

# ----------------------------
# Timestamp & Footer
# ----------------------------
prediction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"<p style='text-align:right; font-size:12px; color:gray;'>Last prediction: {prediction_time}</p>", unsafe_allow_html=True)

st.download_button(
    label="📥 Download Input Summary as CSV",
    data=df_input.to_csv(index=False),
    file_name="heart_attack_input_summary.csv",
    mime="text/csv"
)

st.markdown("""
<hr>
<p style="text-align:center; font-size:14px;">
Made with ❤️ using <b>FastAPI + Streamlit</b> | Developed by <b>Konduru Jayanth</b>
</p>
""", unsafe_allow_html=True)

















