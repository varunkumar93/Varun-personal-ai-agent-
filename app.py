import os
import streamlit as st
from openai import OpenAI

# Set page config
st.set_page_config(page_title="Varun's AI Agent", layout="centered")

# Load API key from secrets
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

# App Title
st.title("🤖 Varun's Personal AI Agent")
st.markdown("Hello 😊 How can I assist you today? 🚀")

# User input
user_input = st.text_input("💬 Your message:", key="user_input_box")

# Handle user message
if st.button("Send") and user_input.strip():
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # New API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")