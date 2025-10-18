import streamlit as st
import requests
import pandas as pd
import datetime

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="🫀 Heart Attack Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #f5f5f5;
    color: #333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sidebar */
.stSidebar .css-1d391kg {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* Header */
h1 {
    color: #2e3a59;
    font-weight: bold;
}

/* Buttons */
.stButton>button {
    background-color: #2e3a59;
    color: white;
    font-size: 16px;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 20px;
    transition: all 0.2s ease;
}
.stButton>button:hover {
    background-color: #1c253b;
}

/* Inputs */
.stNumberInput>div>div>input, .stSelectbox>div>div>select {
    border-radius: 6px;
    padding: 6px;
    border: 1px solid #ccc;
}

/* Input Table */
.table-container table {
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
}
.table-container th, .table-container td {
    border: 1px solid #e0e0e0;
    padding: 8px;
    text-align: center;
}
.table-container th {
    background-color: #2e3a59;
    color: white;
}
.table-container tr:nth-child(even) {
    background-color: #f9f9f9;
}

/* Risk Card */
.risk-card {
    border-radius: 12px;
    padding: 20px;
    color: white;
    font-weight: bold;
    font-size: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar Info
# ----------------------------
st.sidebar.markdown("""
<div>
<p><b>About</b><br>This dashboard predicts the <b>risk of Heart Attack</b> using a trained ML model.</p>
<p><b>Features used:</b><br>- HighBP, HighChol<br>- Smoker, Diabetes<br>- PhysHlth, Sex</p>
<p>Built with <b>FastAPI + Streamlit</b></p>
<p>Developer: <b>Konduru Jayanth</b></p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.markdown('<h1 style="text-align:center;">🫀 Heart Attack Predictor</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:16px; color:#555;">Enter patient details to predict heart disease risk</p>', unsafe_allow_html=True)

# ----------------------------
# Patient Input Section
# ----------------------------
with st.container():
    st.subheader("📋 Patient Information")
    st.caption("⚙️ Input 0 = No, 1 = Yes. Physical Health: 0–30 days")
    col1, col2 = st.columns(2)

    with col1:
        HighBP = st.selectbox("High Blood Pressure", [0,1])
        HighChol = st.selectbox("High Cholesterol", [0,1])
        Smoker = st.selectbox("Smoker", [0,1])

    with col2:
        PhysHlth = st.number_input("Physical Health (0–30 days)", min_value=0, max_value=30, value=5)
        Diabetes = st.selectbox("Diabetes (0=None,1=Type1,2=Type2)", [0,1,2])
        Sex = st.selectbox("Sex (0=Female,1=Male)", [0,1])

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
                    <div class='risk-card' style='background-color:#e74c3c;'>
                        🚨 High Risk! Potential heart disease detected
                        <br><span style="font-size:14px;font-weight:normal;">📝 Tips:<br>- Balanced diet<br>- Exercise<br>- Quit smoking<br>- Regular checkups</span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class='risk-card' style='background-color:#27ae60;'>
                        💚 Low Risk! Heart health looks good
                        <br><span style="font-size:14px;font-weight:normal;">🎉 Tips:<br>- Continue exercise<br>- Eat fruits & vegetables<br>- Maintain healthy weight<br>- Monitor stress</span>
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
# Footer
# ----------------------------
prediction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"<p style='text-align:right; font-size:12px; color:#888;'>Last prediction: {prediction_time}</p>", unsafe_allow_html=True)

st.download_button(
    label="📥 Download Input Summary as CSV",
    data=df_input.to_csv(index=False),
    file_name="heart_attack_input_summary.csv",
    mime="text/csv"
)

st.markdown("""
<hr>
<p style="text-align:center; font-size:14px; color:#555;">
Made with ❤️ using <b>FastAPI + Streamlit</b> | Developed by <b>Konduru Jayanth</b>
</p>
""", unsafe_allow_html=True)
























