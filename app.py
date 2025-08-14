import streamlit as st

st.set_page_config(page_title="Varun's AI Assistant", layout="wide")

# Dark theme styles
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: white;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
        background-color: #121212;
    }
    div[data-testid="stVerticalBlock"] {
        background-color: #121212 !important;
    }
    div[data-testid="stHorizontalBlock"] {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #1E1E1E;
        padding: 0.5rem;
        border-top: 1px solid #333;
    }
    input, textarea {
        background-color: #2C2C2C !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    button {
        background-color: #3C3C3C !important;
        color: white !important;
        border: 1px solid #555 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1 style='text-align:center; color:white;'>🤖 Varun's AI Assistant</h1>", unsafe_allow_html=True)
st.write("---")

# Store messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Dummy AI reply function — replace with actual API call
def get_response(prompt):
    return f"Hello! You said: {prompt}"

# Function to send message
def send_message():
    user_msg = st.session_state.user_input.strip()
    if user_msg:
        st.session_state.messages.append({"role": "user", "content": user_msg})
        ai_reply = get_response(user_msg)
        st.session_state.messages.append({"role": "ai", "content": ai_reply})
        st.session_state.user_input = ""  # Clear input

# Chat history container
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div style='text-align:right;color:#4FC3F7;'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left;color:#81C784;'><b>Varun's AI:</b> {msg['content']}</div>", unsafe_allow_html=True)

# Input + send button at bottom
with st.container():
    col1, col2 = st.columns([8, 1])
    with col1:
        st.text_input("💬 Type your message", key="user_input", on_change=send_message)
    with col2:
        st.button("📩", on_click=send_message)