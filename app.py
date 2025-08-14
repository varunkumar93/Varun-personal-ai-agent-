import streamlit as st
from groq import Groq
import time
from datetime import datetime
import json
import os

# ---------- SETTINGS ----------
st.set_page_config(page_title="Varun's AI Assistant", layout="centered")

st.markdown("""
<style>
body { background-color: #000; color: #fff; }
div.stTextInput>div>div>input {
    background-color: #222 !important;
    color: #fff !important;
    border-radius: 8px;
    border: 1px solid #444;
    padding: 6px;
}
div.stButton>button {
    background-color: #444 !important;
    color: #fff !important;
    border-radius: 8px;
    border: 1px solid #555;
}
.chat-message {
    padding: 8px;
    border-radius: 8px;
    margin-bottom: 5px;
    word-wrap: break-word;
    max-width: 80%;
}
.user-message {
    color: #4DB8FF;
    text-align: right;
    margin-left: auto;
    background-color: #111;
}
.ai-message {
    color: #90EE90;
    text-align: left;
    margin-right: auto;
    background-color: #111;
}
.timestamp {
    font-size: 10px;
    color: #888;
    display: block;
    margin-top: 2px;
}
#chat-container {
    height: 65vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    padding-right: 5px;
}
</style>
""", unsafe_allow_html=True)

# ---------- API CLIENT ----------
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# ---------- APP TITLE ----------
st.title("🤖 Varun's AI Assistant")

# ---------- AI PERSONALITIES ----------
personalities = {
    "Friendly": "You are a friendly and casual AI assistant. Use emojis freely.",
    "Professional": "You are a professional AI assistant giving precise answers.",
    "Funny": "You are a humorous AI assistant, adding light jokes and emojis.",
}
ai_style = st.selectbox("Choose AI Personality", list(personalities.keys()), index=0)

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- LOAD PERSISTENT CHAT HISTORY ----------
HISTORY_FILE = "chat_history.json"
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        st.session_state.messages = json.load(f)

# ---------- FUNCTION TO SAVE CHAT HISTORY ----------
def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)

# ---------- FUNCTION TO GET AI RESPONSE ----------
def get_ai_response(prompt, personality_prompt):
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": personality_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return chat_completion.choices[0].message.content

# ---------- DISPLAY CHAT ----------
def display_chat():
    chat_html = "<div id='chat-container'>"
    for msg in st.session_state.messages:
        timestamp = msg.get("time", "")
        if msg["role"] == "user":
            chat_html += f"<div class='chat-message user-message'><b>You:</b> {msg['content']}<span class='timestamp'>{timestamp}</span></div>"
        else:
            chat_html += f"<div class='chat-message ai-message'><b>Varun's AI:</b> {msg['content']}<span class='timestamp'>{timestamp}</span></div>"
    chat_html += "<div id='bottom'></div></div>"
    st.markdown(chat_html, unsafe_allow_html=True)
    st.markdown("<script>document.getElementById('bottom').scrollIntoView({behavior: 'smooth'});</script>", unsafe_allow_html=True)

display_chat()

# ---------- INPUT AREA WITH FORM ----------
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])
    with col1:
        user_input = st.text_input("💬 Type your message", label_visibility="collapsed")
    with col2:
        send_clicked = st.form_submit_button("📩 Send")

    if send_clicked and user_input.strip():
        # Add user message with timestamp
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": datetime.now().strftime("%H:%M")
        })
        save_history()
        display_chat()

        # Placeholder for AI typing
        placeholder = st.empty()
        placeholder.markdown("<div class='chat-message ai-message'><b>Varun's AI:</b> Typing...</div>", unsafe_allow_html=True)
        time.sleep(0.8)

        # Get AI response
        ai_reply = get_ai_response(user_input, personalities[ai_style])

        # Typing animation
        typed_text = ""
        for char in ai_reply:
            typed_text += char
            placeholder.markdown(
                f"<div class='chat-message ai-message'><b>Varun's AI:</b> {typed_text}<span class='timestamp'>{datetime.now().strftime('%H:%M')}</span></div>",
                unsafe_allow_html=True
            )
            time.sleep(0.02)

        # Save AI reply
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_reply,
            "time": datetime.now().strftime("%H:%M")
        })
        save_history()
        st.experimental_rerun()