import streamlit as st
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline


data = pd.read_csv(r"C:\Users\mateu\PycharmProjects\ProjektAnalizaEmocji\emotion_dataset.csv")

X = data["text"]
Y = data["emotion"]

model = make_pipeline(CountVectorizer(), LogisticRegression(max_iter=1000))
model.fit(X, Y)

model_file_path = "emotion_detection_model.pkl"
try:
    with open(model_file_path, 'rb'):
        pass
except FileNotFoundError:
    joblib.dump(model, model_file_path)


def predict_emotions(text):
    prediction = model.predict([text])[0]
    return prediction


st.title("Analiza emocji")
text_input = st.text_area("Wprowadź text:")
if st.button("Analizuj"):
    if text_input:
        emotion = predict_emotions(text_input)
        st.write(f"Najbardziej prawdopodobna emocja: {emotion}")
    else:
        st.error("Wprowadź tekst przed kliknięciem przycisku Analizuj!")