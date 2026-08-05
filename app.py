import streamlit as st
from chatbot.memory import initialize_chat, add_message, get_messages
from chatbot.response import get_ai_response

st.set_page_config(
    page_title="MediAssistAI - Healthcare Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        max-width: 900px;
        margin: 0 auto;
    }
    .stChatMessage {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
col1, col2 = st.columns([0.2, 0.8])
with col1:
    st.image("https://img.icons8.com/color/96/000000/hospital.png", width=80)
with col2:
    st.title("MediAssistAI")
    st.caption("Your AI Healthcare Assistant 🏥 | Ask any health-related question")

st.divider()

initialize_chat()

# Display chat history
for message in get_messages():
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me about health, nutrition, exercise, symptoms...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    add_message("user", prompt)

    # Get AI response
    with st.spinner("🤔 Analyzing your question..."):
        answer = get_ai_response(get_messages())

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(answer)

    add_message("assistant", answer)

# Footer with suggestions
st.divider()
st.markdown("""
**Sample questions you can ask:**
- What are the symptoms of diabetes?
- How much water should I drink daily?
- What's a healthy BMI range?
- Tips for better sleep
- How to manage stress naturally?
""")
