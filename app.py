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
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

message = st.text_area(
    "Enter Your Message",
    key="input_text"
)
col1, col2 = st.columns([9,1])
with col1:
    check_clicked = st.button("Check Message")

with col2:
   if st.button("🗑"):
    del st.session_state["input_text"]
    st.rerun()

# Prediction
if check_clicked:

    if message.strip() == "":
        st.warning("Please enter a message")

    else:

        with st.spinner("Analyzing message with AI..."):


            # Detect suspicious links
            suspicious_links = re.findall(r'(https?://\S+|www\.\S+)', message)

            #trusted Domain Detection
            trusted_domains = [
                "youtube.com",
                "google.com",
                "github.com",
                "amazon.com",
                "microsoft.com",
                "openai.com",
                "wikipedia.org"
            ]
            safe_link_detected = False

            for domain in trusted_domains:
                if domain in message.lower():
                    safe_link_detected = True

            # Fake Domain Detection
            fake_domains = [
                ".xyz",
                ".ru",
                "secure-login",
                "verify-account",
                "free-money",
                "paypal-secure",
                "banking-verification",
            ]

            fake_domain_detected = False

            for domain in fake_domains:
                if domain.lower() in message.lower():
                    fake_domain_detected = True

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
            # Final Smart Decision Logic

            final_prediction = prediction[0]



            # Override if phishing detected
            if phishing_detected or suspicious_links:
                final_prediction = 1

            if suspicious_links:
                risk_score += 30

            if phishing_detected:
                 risk_score += 25


            # Increase confidence
            confidence = min(confidence + risk_score, 100)
            # Confidence Progress Bar
            st.progress(int(confidence))

            st.markdown(f"""
            ### 🔐 Security Confidence Score: {confidence}%
            """)



            # Risk Level Logic
            risk_level = "SAFE"
            risk_color = "green"

            if final_prediction == 1 and confidence > 80:
                risk_level = "DANGEROUS"
                risk_color = "red"

            elif phishing_detected or fake_domain_detected or (suspicious_links and not safe_link_detected):
                risk_level = "SUSPICIOUS"
                risk_color = "orange"

                # Risk Level Display
                st.markdown(f"""
                <div style="
                    background-color:{risk_color};
                    padding:12px;
                    border-radius:10px;
                    color:white;
                    font-size:22px;
                    font-weight:bold;
                    text-align:center;
                    margin-top:15px;">
                    
                    🚨 RISK LEVEL: {risk_level}

                </div>
                """, unsafe_allow_html=True)



             # Warning Messages
            if suspicious_links and not safe_link_detected:
                st.warning("⚠ Suspicious Link Detected!")

            if phishing_detected:
                st.warning("⚠ Possible Phishing Attempt!")




            # Threat Analysis Panel

            threats = []

            if suspicious_links:
                threats.append("✔ Suspicious link detected")

            if phishing_detected:
                threats.append("✔ Possible phishing keywords found")

            if fake_domain_detected:
                threats.append("✔ Fake or malicious domain detected")

            if "bank" in message.lower():
                threats.append("✔ Banking-related content detected")

            if "urgent" in message.lower():
                threats.append("✔ Urgent tone detected")

            if "verify" in message.lower():
                threats.append("✔ Verification request detected")

            if "login" in message.lower():
                threats.append("✔ Login request detected")




            # Display Threat Analysis
            st.markdown("## 🛡 Threat Analysis")

            if threats:
                for threat in threats:
                    st.warning(threat)
            else:
                st.success("✔ No suspicious activity found")

            if final_prediction == 1:
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
          