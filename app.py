import streamlit as st
import pickle

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

        prediction = model.predict([message])

        if prediction[0] == 1:
            st.error("Spam Message Detected")
        else:
            st.success("Safe Message")