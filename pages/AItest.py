import streamlit as st
import google.generativeai as genai

genai.configure(
    api_key=st.secrets[google]["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("AI Test")

question = st.text_input("Ask something")

if st.button("Run"):
    response = model.generate_content(question)
    st.write(response.text)
