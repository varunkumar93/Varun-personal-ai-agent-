import streamlit as st
from groq import Groq
import time
from datetime import datetime
import json
import os

# ---------- SETTINGS ----------
st.set_page_config(page_title="Varun's AI Assistant", layout="centered")

with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- API CLIENT ----------
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# ---------- USER PROFILE ----------
def load_user_profile():
    if os.path.exists("user_profile.json"):
        with open("user_profile.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

user_profile = load_user_profile()

# ---------- AI PERSONALITIES ----------
personalities = {
    "Friendly": "You are a friendly and casual AI assistant. Use emojis freely.",
    "Professional": "You are a professional AI assistant giving precise answers.",
    "Funny": "You are a humorous AI assistant, adding light jokes and emojis.",
    "Spiritual Guide": "You are a wise and gentle assistant who shares spiritual insights and devotional inspiration.",
    "Tech Mentor": "You are a practical and encouraging assistant who helps users learn machine learning and build projects."
}
ai_style = st.selectbox("Choose AI Personality", list(personalities.keys()), index=0)

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- LOAD CHAT HISTORY ----------
HISTORY_FILE = "chat_history.json"
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        st.session_state.messages = json.load(f)

# ---------- SAVE CHAT HISTORY ----------
def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)

# ---------- GET AI RESPONSE ----------
def get_ai_response(prompt, personality_prompt, user_profile):
    context = f"""
You are Varun's AI Assistant. Your user is {user_profile.get('name', 'a curious person')}.
They are interested in {', '.join(user_profile.get('interests', []))}.
Their goals include {', '.join(user_profile.get('goals', []))}.
Your tone should be {user_profile.get('tone', 'friendly and helpful')}.
Respond in the style: {personality_prompt}
"""
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": context},
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

# ---------- INPUT FORM ----------
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])
    with col1:
        user_input = st.text_input("💬 Type your message", label_visibility="collapsed")
    with col2:
        send_clicked = st.form_submit_button("📩 Send")

    if send_clicked and user_input.strip():
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "time": datetime.now().strftime("%H:%M")
        })
        save_history()
        display_chat()

        placeholder = st.empty()
        placeholder.markdown("<div class='chat-message ai-message'><b>Varun's AI:</b> Typing...</div>", unsafe_allow_html=True)
        time.sleep(0.8)

        ai_reply = get_ai_response(user_input, personalities[ai_style], user_profile)

        typed_text = ""
        for char in ai_reply:
            typed_text += char
            placeholder.markdown(
                f"<div class='chat-message ai-message'><b>Varun's AI:</b> {typed_text}<span class='timestamp'>{datetime.now().strftime('%H:%M')}</span></div>",
                unsafe_allow_html