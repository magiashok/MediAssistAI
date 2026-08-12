from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

# Try to get API key from Streamlit secrets first (for cloud deployment)
# Fall back to .env file (for local development)
#
# Note: st.secrets raises StreamlitSecretNotFoundError (rather than just
# acting like an empty dict) when no secrets.toml file exists at all — which
# is the normal case for local development. Wrapping this in try/except lets
# it fall through to the .env file instead of crashing on startup.
api_key = None
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)