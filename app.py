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
    background: linear-gradient(135deg, #fff0f3, #ffe8e8);
    color: #333;
    font-family: 'Arial', sans-serif;
}

/* Sidebar card */
.stSidebar .css-1d391kg {
    background: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.1);
}

/* Header */
h1 {
    color: #d63447;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #ff6b6b, #ff4757);
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 25px;
    transition: all 0.2s ease;
}
.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #ff4757, #ff6b6b);
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
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.table-container th, .table-container td {
    border: 1px solid #f2f2f2;
    padding: 10px;
    text-align: center;
}
.table-container th {
    background-color: #ffd6d6;
    color: #333;
}
.table-container tr:nth-child(even) {
    background-color: #fff0f3;
}

/* Risk Card */
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
<p>Developer: <b>Konduru Jayanth</b></p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.markdown('<h1 style="text-align:center;">🫀 Heart Attack Predictor</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:18px;">Enter patient details to predict heart disease risk</p>', unsafe_allow_html=True)

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
                    <div class='risk-card' style='background: linear-gradient(135deg, #ff6b6b, #ff4757);'>
                        🚨 High Risk! Potential heart disease detected
                        <br><span style="font-size:15px;font-weight:normal;">📝 Tips:<br>- Balanced diet<br>- Exercise<br>- Quit smoking<br>- Checkups</span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class='risk-card' style='background: linear-gradient(135deg, #6bc1ff, #1f90ff);'>
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
# Footer
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




















