import streamlit as st

st.title("PDF Question Answering Chatbot")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

if uploaded_file:
    st.success("PDF uploaded successfully!")
    