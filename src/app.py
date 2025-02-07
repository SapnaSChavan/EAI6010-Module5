from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import os

# ✅ Load the trained model and vectorizer
try:
    # Load the trained model and vectorizer
    model_path = os.path.join(os.path.dirname(__file__), "model")
    model = joblib.load(os.path.join(model_path, "svm_model.pkl"))
    vectorizer = joblib.load(os.path.join(model_path, "tfidf_vectorizer.pkl"))
    
except FileNotFoundError:
    raise RuntimeError("Missing model files. Ensure 'svm_model.pkl' and 'tfidf_vectorizer.pkl' are present.")

# Initialize FastAPI app
app = FastAPI()

# Define input format
class TextInput(BaseModel):
    text: str

@app.post("/predict/")
def predict_spam(input_data: TextInput):
    try:
        # Transform input text
        text_vectorized = vectorizer.transform([input_data.text])

        # Predict using the model
        prediction = model.predict(text_vectorized)[0]

        # Return result
        return {"input_text": input_data.text, "prediction": "spam" if prediction == 1 else "not spam"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # ✅ Fix for Windows Users
    import sys
    import asyncio
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # ✅ Start FastAPI Server
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
