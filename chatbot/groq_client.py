from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

# Try to get API key from Streamlit secrets first (for cloud deployment)
# Fall back to .env file (for local development)
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)