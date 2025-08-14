import streamlit as st
from groq import Groq
import time
from datetime import datetime
import json
import os

# ---------- SETTINGS ----------
st.set_page_config(page_title="Varun's AI Assistant", layout="centered")

# ---------- THEME TOGGLE ----------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

theme_choice = st.radio("Choose Theme", ["🌙 Dark", "☀️ Light"], horizontal=True)
st.session_state.theme = "dark" if "Dark" in theme_choice else "light"

# ---------- INLINE CSS ----------
def get_css(theme):
    if theme == "dark":
        return """
        <style>
        body { background-color: #000; color: #fff; }
        .chat-message { background-color: #2ca02c; color: white; border-radius: 8px; padding: 8px; margin-bottom: 10px; }
        .user-message { background-color: #1f77b4; color: white; border-radius: 8px; padding: 8px; margin-bottom: 10px; text-align: right; }
        #input-area { background-color: #000; border-top: 1px solid #333; padding: 10px; }
        </style>
        """
    else:
        return """
        <style>
        body { background-color: #f5f5f5; color: #000; }
        .chat-message { background-color: #dff0d8; color: #000; border-radius: 8px; padding: 8px; margin-bottom: 10px; }
        .user-message { background-color: #cce5ff; color: #000; border-radius: 8px; padding: 8px; margin-bottom: 10px; text-align: right; }
        #input-area { background-color: #fff; border-top: 1px solid #ccc; padding: 10px; }
        </style>
        """

st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

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
HISTORY