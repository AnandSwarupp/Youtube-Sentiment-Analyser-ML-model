import joblib
import os

MODEL_PATH = os.path.join("model", "sentiment_model.pkl")

model = joblib.load(MODEL_PATH)
