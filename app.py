import streamlit as st
from chatbot.memory import initialize_chat, add_message, get_messages, clear_chat
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
col1, col2, col3 = st.columns([0.15, 0.65, 0.2])
with col1:
    st.image("https://img.icons8.com/color/96/000000/hospital.png", width=80)
with col2:
    st.title("MediAssistAI")
    st.caption("Your AI Healthcare Assistant 🏥 | Ask any health-related question")
with col3:
    st.write("")  # vertical spacer to align button with title
    if st.button("🔄 New Chat", use_container_width=True):
        clear_chat()
        st.rerun()

st.divider()

initialize_chat()

# Cap on questions per session so one visitor can't drain the shared API key.
# Counting "user" messages already in history means this needs no extra state.
MAX_QUESTIONS_PER_SESSION = 15

# Display chat history
for message in get_messages():
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

questions_asked = len([m for m in get_messages() if m["role"] == "user"])
questions_left = max(MAX_QUESTIONS_PER_SESSION - questions_asked, 0)
st.caption(f"💬 {questions_left}/{MAX_QUESTIONS_PER_SESSION} questions left this session")

# Chat input
prompt = st.chat_input("Ask me about health, nutrition, exercise, symptoms...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    add_message("user", prompt)

    if questions_asked >= MAX_QUESTIONS_PER_SESSION:
        answer = (
            f"🙏 You've reached the {MAX_QUESTIONS_PER_SESSION}-question limit for this session, "
            "to keep this free and available for everyone. Click **🔄 New Chat** above to start "
            "a fresh session, or check back again later."
        )
    else:
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
