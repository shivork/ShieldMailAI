import streamlit as st
import pickle
import re

# Load model
model = pickle.load(open("spam_model.pkl", "rb"))

# Page settings
st.set_page_config(
    page_title="ShieldMail AI",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}

.stTextArea textarea {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
    border: 2px solid #38bdf8;
}

.stButton button {
    background-color: #38bdf8;
    color: black;
    font-weight: bold;
    border-radius: 10px;
    height: 50px;
    width: 100%;
}

.result-box {
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🛡️ ShieldMail AI")
st.subheader("Advanced Spam Email Detection System")

# Input
message = st.text_area("Enter Your Message")

# Prediction
if st.button("Check Message"):

    if message.strip() == "":
        st.warning("Please enter a message")

    else:

        with st.spinner("Analyzing message with AI..."):
            # Detect suspicious links
            suspicious_links = re.findall(r'(https?://\S+|www\.\S+)', message)

            phishing_words = [
                "login",
                "verify",
                "bank",
                "claim",
                "reward",
                "winner",
                "free",
                "urgent",
                "click"
           ]

            phishing_detected = False

            for word in phishing_words:
                if word.lower() in message.lower():
                  phishing_detected = True

            prediction = model.predict([message])

            probability = model.predict_proba([message])

            confidence = round(max(probability[0]) * 100, 2)
            # Risk score boost
            risk_score = 0

            if suspicious_links:
                risk_score += 30

            if phishing_detected:
                 risk_score += 25

             # Increase confidence
            confidence = min(confidence + risk_score, 100)

            # Risk Level Logic
            risk_level = "SAFE"
            risk_color = "green"

            if prediction[0] == 1 and confidence > 80:
                risk_level = "DANGEROUS"
                risk_color = "red"

            elif phishing_detected or suspicious_links:
                risk_level = "SUSPICIOUS"
                risk_color = "orange"

            # Warning Messages
            if suspicious_links:
                st.warning("⚠ Suspicious Link Detected!")

            if phishing_detected:
                st.warning("⚠ Possible Phishing Attempt!")

            if prediction[0] == 1 or phishing_detected:
                st.markdown(f"""
                    <div style="
                    background: linear-gradient(90deg,#ff4b2b,#ff416c);
                    padding:20px;
                    border-radius:15px;
                    color:white;
                    font-size:24px;
                    font-weight:bold;
                    text-align:center;
                    margin-top:20px;">
                    🚨 SPAM MESSAGE<br>
                    Confidence: {confidence}%
                    </div>
                    """, unsafe_allow_html=True)

            else:

                st.markdown(f"""
                    <div style="
                    background: linear-gradient(90deg,#00ff87,#60efff);
                    padding:20px;
                    border-radius:15px;
                    color:black;
                    font-size:24px;
                    font-weight:bold;
                    text-align:center;
                    margin-top:20px;">
                    ✅ SAFE MESSAGE<br>
                    Confidence: {confidence}%
                    </div>
                    """, unsafe_allow_html=True)