import streamlit as st
import requests

# Set API URL
API_URL = "https://eai6010-youtube-comment-spam-classifier.onrender.com/predict/"

# Custom Styling for Title and Layout
st.markdown(
    """
    <style>
    .main {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1 {
        font-size: 38px !important; 
        color: #333333;            
        text-align: left;
    }
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 10px 20px;
    }
    div.stButton > button:first-child:hover {
        background-color: #ff0000;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section
st.title("📺 YouTube Comment Spam Classifier")
st.write("Detect whether a YouTube comment is spam or not!")

# Input Section
user_input = st.text_area("Enter YouTube comment here:", "")

# Predict Button
if st.button("Check Spam"):
    if user_input.strip():
        # Make API call
        response = requests.post(API_URL, json={"text": user_input})
        if response.status_code == 200:
            result = response.json()
            prediction = result["prediction"].upper()
            if prediction == "SPAM":
                st.success(f"🎯 Prediction: {prediction} ✅")
            else:
                st.info(f"🛡️ Prediction: {prediction} ✅")
        else:
            st.error("❌ Error connecting to API. Make sure FastAPI is running!")
    else:
        st.warning("⚠️ Please enter a comment before submitting!")
