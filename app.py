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