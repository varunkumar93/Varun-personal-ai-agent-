import streamlit as st
from groq import Groq
import time
from datetime import datetime
import json
import os
import pandas as pd

# ---------- SETTINGS ----------
st.set_page_config(page_title="Varun's AI Assistant", layout="centered")

# ---------- THEME TOGGLE ----------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

theme_choice = st.radio("Choose Theme", ["🌙 Dark", "☀️ Light"], horizontal=True, key="theme_toggle")
# ---------- INLINE CSS ----------
def get_css(theme):
    return """
    <style>
    body { background-color: %s; color: %s; }
    .chat-message { background-color: %s; color: %s; border-radius: 8px; padding: 8px; margin-bottom: 10px; }
    .user-message { background-color: %s; color: %s; border-radius: 8px; padding: 8px; margin-bottom: 10px; text-align: right; }
    #input-area { background-color: %s; border-top: 1px solid %s; padding: 10px; }
    </style>
    """ % (
        "#000" if theme == "dark" else "#f5f5f5",
        "#fff" if theme == "dark" else "#000",
        "#2ca02c" if theme == "dark" else "#dff0d8",
        "white" if theme == "dark" else "#000",
        "#1f77b4" if theme == "dark" else "#cce5ff",
        "white" if theme == "dark" else "#000",
        "#000" if theme == "dark" else "#fff",
        "#333" if theme == "dark" else "#ccc"
    )

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

# ---------- PERSONALITIES ----------
personalities = {
    "Friendly": "You are a friendly and casual AI assistant. Use emojis freely.",
    "Professional": "You are a professional AI assistant giving precise answers.",
    "Funny": "You are a humorous AI assistant, adding light jokes and emojis.",
    "Spiritual Guide": "You are a wise and gentle assistant who shares spiritual insights and devotional inspiration.",
    "Tech Mentor": "You are a practical and encouraging assistant who helps users learn machine learning and build projects."
}
ai_style = st.selectbox("Choose AI Personality", list(personalities.keys()), index=0, key="ai_personality_select")

# ---------- SESSION ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- AI RESPONSE ----------
def get_ai_response(prompt, personality_prompt, user_profile):
    context = (
        f"You are Varun's AI Assistant. Your user is {user_profile.get('name', 'a curious person')}.\n"
        f"They are interested in {', '.join(user_profile.get('interests', []))}.\n"
        f"Their goals include {', '.join(user_profile.get('goals', []))}.\n"
        f"Your tone should be {user_profile.get('tone', 'friendly and helpful')}.\n"
        f"Respond in the style: {personality_prompt}"
    )
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )
    return chat_completion.choices[0].message.content

# ---------- CHAT DISPLAY ----------
st.markdown("### 💬 Chat with Varun's Assistant")
for msg in st.session_state.messages:
    role_class = "user-message" if msg["role"] == "user" else "chat-message"
    st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# ---------- TEXT INPUT ----------
st.markdown("<div id='input-area'>", unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([1, 9])
    with col1:
        send_clicked = st.form_submit_button("📩", use_container_width=True)
    with col2:
        user_input = st.text_input("Type your message...", label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

if send_clicked and user_input.strip():
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": datetime.now().strftime("%H:%M")
    })
    placeholder = st.empty()
    placeholder.markdown("<div class='chat-message'><b>Varun's AI:</b> Typing...</div>", unsafe_allow_html=True)
    time.sleep(0.8)
    ai_reply = get_ai_response(user_input, personalities[ai_style], user_profile)
    typed_text = ""
    for char in ai_reply:
        typed_text += char
        placeholder.markdown(f"<div class='chat-message'>{typed_text}</div>", unsafe_allow_html=True)
        time.sleep(0.02)
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply,
        "time": datetime.now().strftime("%H:%M")
    })
    st.rerun()

# ---------- FILE UPLOAD ----------
with st.expander("📁 File Upload & Summarization"):
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "csv"])
    def summarize_file(file):
        if file.type == "text/plain":
            content = file.read().decode("utf-8")
            prompt = f"Please summarize the following text:\n\n{content[:3000]}"
            return get_ai_response(prompt, personalities[ai_style], user_profile)
        elif file.type == "text/csv":
            df = pd.read_csv(file)
            prompt = f"Summarize this CSV file with columns: {', '.join(df.columns)} and {len(df)} rows."
            return get_ai_response(prompt, personalities[ai_style], user_profile)
        else:
            return "Unsupported file type."
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        summary = summarize_file(uploaded_file)
        st.markdown(f"<div class='chat-message'>{summary}</div>", unsafe_allow_html=True)

# ---------- CODE ASSISTANT ----------
with st.expander("🧑‍💻 Code Assistant"):
    def detect_language(code):
        if "def " in code or "import " in code:
            return "Python"
        elif "function " in code or "console.log" in code:
            return "JavaScript"
        elif "#include" in code or "int main()" in code:
            return "C++"
        elif "<html>" in code or "<div>" in code:
            return "HTML"
        else:
            return "Unknown"

    with st.form("code_form", clear_on_submit=True):
        code_input = st.text_area("Paste your code here...", height=200)
        mode = st.selectbox("Choose Mode", ["Explain", "Debug", "Optimize"], key="code_mode")
        save_code = st.checkbox("💾 Save this snippet")
        code_submit = st.form_submit_button("🚀 Run")

    if code_submit and code_input.strip():
        lang = detect_language(code_input)
        prompt = f"You are a helpful coding assistant. The user pasted {lang} code and wants you to {mode.lower()} it:\n\n{code_input}"
        st.session_state.messages.append({
            "role": "user",
            "content": f"{mode} this {lang} code:\n\n{code_input}",
            "time": datetime.now().strftime("%H:%M")
        })
        placeholder = st.empty()
        placeholder.markdown(f"<div class='chat-message'><b>Varun's AI:</b> {mode} in progress...</div>", unsafe_allow_html=True)
        time.sleep(0.8)
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


# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- FILE SUMMARIZATION ----------
def summarize_file(file):
    if file.type == "text/plain":
        content = file.read().decode("utf-8")
        prompt = f"Please summarize the following text:\n\n{content[:3000]}"
        return get_ai_response(prompt, personalities[ai_style], user_profile)
    elif file.type == "text/csv":
        df = pd.read_csv(file)
        summary_prompt = f"Summarize this CSV file with columns: {', '.join(df.columns)} and {len(df)} rows."
        return get_ai_response(summary_prompt, personalities[ai_style], user_profile)
    else:
        return "Unsupported file type for summarization."

# ---------- LANGUAGE DETECTION ----------
def detect_language(code):
    if "def " in code or "import " in code:
        return "Python"
    elif "function " in code or "console.log" in code:
        return "JavaScript"
    elif "#include" in code or "int main()" in code:
        return "C++"
    elif "<html>" in code or "<div>" in code:
        return "HTML"
    else:
        return "Unknown"
