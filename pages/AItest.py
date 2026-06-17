import streamlit as st
import google.generativeai as genai

genai.configure(
    api_key=st.secrets["google"]["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("AI Test")

if st.button("Test AI"):
    response = model.generate_content(
        "Say hello in Thai."
    )

    st.write(response.text)
