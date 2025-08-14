
import streamlit as st

st.set_page_config(page_title="Varun's AI Agent", layout="wide")

# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_response(prompt):
    # Dummy AI logic - replace with your API call
    return f"Echo: {prompt}"

def send_message():
    if st.session_state.user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
        
        # Get AI reply
        reply = get_response(st.session_state.user_input)
        st.session_state.messages.append({"role": "ai", "content": reply})
        
        # Clear text box
        st.session_state.user_input = ""

# Chat container
chat_container = st.container()

# Scrollable area for messages
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div style='text-align:right;color:blue;'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left;color:green;'><b>AI:</b> {msg['content']}</div>", unsafe_allow_html=True)

# Fixed input area at bottom
st.markdown(
    """
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    .stTextInput {position: fixed; bottom: 0; width: 100%;}
    </style>
    """,
    unsafe_allow_html=True
)

st.text_input("💬 Type your message", key="user_input", on_change=send_message)