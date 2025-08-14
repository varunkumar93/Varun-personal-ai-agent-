import streamlit as st

st.set_page_config(page_title="Varun's AI Agent", layout="wide")

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_response(prompt):
    # Dummy AI response — replace with your actual API call
    return f"Echo: {prompt}"

def send_message():
    user_msg = st.session_state.user_input.strip()
    if user_msg:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_msg})
        # Get AI response
        ai_reply = get_response(user_msg)
        st.session_state.messages.append({"role": "ai", "content": ai_reply})
        # Clear input
        st.session_state.user_input = ""

# Chat history container
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div style='text-align:right;color:blue;'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left;color:green;'><b>AI:</b> {msg['content']}</div>", unsafe_allow_html=True)

# Fixed input + button at bottom
st.markdown(
    """
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 5rem;}
    div[data-testid="stHorizontalBlock"] {position: fixed; bottom: 0; left: 0; width: 100%; background: white; padding: 0.5rem; border-top: 1px solid #ddd;}
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    col1, col2 = st.columns([8, 1])
    with col1:
        st.text_input("💬 Type your message", key="user_input", on_change=send_message)
    with col2:
        st.button("Send", on_click=send_message)