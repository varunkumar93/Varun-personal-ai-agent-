import streamlit as st
from groq import Groq

# Page config
st.set_page_config(page_title="🤖 Varun's Personal AI Agent", layout="centered")
st.title("🤖 Varun's Personal AI Agent")
st.markdown("Hello 😊 How can I assist you today? 🚀")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Groq client (reads key from Streamlit Secrets)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# User input
user_message = st.text_input("💬 Your message:", key="user_input")

# When user sends a message
if st.button("Send"):
    if user_message.strip():
        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_message})

        try:
            # Get Groq AI response
            chat_completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages
            )
            bot_reply = chat_completion.choices[0].message.content

            # Save bot message
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            bot_reply = f"⚠️ Error: {e}"
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")