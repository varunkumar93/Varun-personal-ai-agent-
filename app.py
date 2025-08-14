import streamlit as st
import openai
import datetime

# ✅ Page config
st.set_page_config(page_title="🤖 Varun's Personal AI Agent", layout="centered")

# ✅ OpenAI API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ✅ AI function
def get_ai_reply(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Varun's helpful personal AI assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response["choices"][0]["message"]["content"].strip()

# ✅ Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_message" not in st.session_state:
    st.session_state.user_message = ""

# ✅ Function to handle sending message
def send_message():
    if st.session_state.user_message.strip():
        current_time = datetime.datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append(("You", st.session_state.user_message, current_time))
        
        bot_reply = get_ai_reply(st.session_state.user_message)
        st.session_state.chat_history.append(("Bot", bot_reply, current_time))
        
        st.session_state.user_message = ""  # ✅ safe to reset here

# ✅ Title
st.title("🤖 Varun's Personal AI Agent")

# ✅ Chat display
for sender, message, time in st.session_state.chat_history:
    st.markdown(f"**{sender}** ({time}): {message}")

# ✅ Input & send
st.text_input("💬 Your message:", key="user_message", on_change=send_message)