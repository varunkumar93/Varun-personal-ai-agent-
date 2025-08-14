import streamlit as st
import openai
import datetime

# ✅ Set Streamlit page settings
st.set_page_config(page_title="🤖 Varun's Personal AI Agent", layout="centered")

# ✅ Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ✅ AI Response Function
def get_ai_reply(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Change to "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are Varun's helpful personal AI assistant."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"].strip()

# ✅ Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ App title
st.title("🤖 Varun's Personal AI Agent")
st.markdown("Hello 😊 How can I assist you today? 🚀")

# ✅ Input box
user_input = st.text_input("💬 Your message:")

# ✅ Send button
if st.button("Send"):
    if user_input.strip():
        current_time = datetime.datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append(("You", user_input, current_time))

        bot_reply = get_ai_reply(user_input)
        st.session_state.chat_history.append(("Bot", bot_reply, current_time))

        # Clear text box by rerunning with empty input
        st.experimental_rerun()

# ✅ Chat history display
for sender, message, time in st.session_state.chat_history:
    st.markdown(f"**{sender}** ({time}): {message}")