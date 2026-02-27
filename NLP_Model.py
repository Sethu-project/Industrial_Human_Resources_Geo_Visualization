import streamlit as st
import pickle

st.set_page_config(page_title="Industry NLP Classifier", layout="wide")

st.title("🏭 Industry Sector NLP Classifier")

# ------------------------------
# Load Model
# ------------------------------
model = pickle.load(open("D:\GUVI DS 2025\Industrial HR Geo Project\industry_classifier.pkl", "rb"))
vectorizer = pickle.load(open("D:\\GUVI DS 2025\\Industrial HR Geo Project\\tfidf_vectorizer.pkl", "rb"))
#vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
#model = pickle.load(open("industry_classifier.pkl", "rb"))
# ------------------------------
# User Input
# ------------------------------
user_input = st.text_area("Enter NIC Description")

if st.button("Predict Industry"):
    if user_input.strip() == "":
        st.warning("Please enter industry description.")
    else:
        vec = vectorizer.transform([user_input])
        prediction = model.predict(vec)[0]
        st.success(f"Predicted Industry Sector: {prediction}")