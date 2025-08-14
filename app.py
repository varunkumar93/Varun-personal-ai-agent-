import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Varun's AI Agent", layout="centered")
st.title("🤖 Varun's Personal AI Agent")
st.markdown("Ask me anything — coding, QA, mock interviews, productivity tips!")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Varun's helpful assistant.", "time": datetime.now().strftime("%H:%M")}
    ]

# User & Bot profile image URLs
USER_ICON = "https://cdn-icons-png.flaticon.com/512/847/847969.png"  # Replace with your photo URL if you want
BOT_ICON = "https://cdn-icons-png.flaticon.com/512/4712/4712109.png"

def get_response():
    headers = {
        "Authorization": f"Bearer {st.secrets['openrouter_key']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-medium-3.1",
        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"] != "system"],
        "max_tokens": 2000
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        result = response.json()
    except Exception as e:
        return f"❌ Network Error: {e}"

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    elif "error" in result:
        return f"⚠️ API Error: {result['error']}"
    else:
        return "⚠️ Unexpected API response. Please check your API key and model name."

# Function to style chat bubbles with profile icons
def chat_bubble(content, time, role):
    if role == "user":
        bg_color = "#DCF8C6"  # WhatsApp green
        align = "flex-end"
        icon_url = USER_ICON
    else:
        bg_color = "#F1F0F0"  # WhatsApp gray
        align = "flex-start"
        icon_url = BOT_ICON

    bubble_html = f"""
    <div style="display: flex; align-items: flex-end; justify-content: {align}; margin-bottom: 10px;">
        {'<img src="' + icon_url + '" style="width:35px;height:35px;border-radius:50%;margin-right:5px;">' if role == 'assistant' else ''}
        <div style="
            background-color: {bg_color};
            padding: 10px;
            border-radius: 10px;
            max-width: 70%;
            ">
            {content}
            <div style="text-align: right; font-size: 0.8em; color: gray;">{time}</div>
        </div>
        {'<img src="' + icon_url + '" style="width:35px;height:35px;border-radius:50%;margin-left:5px;">' if role == 'user' else ''}
    </div>
    """
    return bubble_html

# Display chat history (excluding system message)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.markdown(chat_bubble(msg['content'], msg['time'], msg['role']), unsafe_allow_html=True)

# Chat input at the bottom
if prompt := st.chat_input("Type your message here..."):
    current_time = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": prompt, "time": current_time})
    st.markdown(chat_bubble(prompt, current_time, "user"), unsafe_allow_html=True)

    with st.spinner("Thinking..."):
        reply_time = datetime.now().strftime("%H:%M")
        reply = get_response()
        st.session_state.messages.append({"role": "assistant", "content": reply, "time": reply_time})
        st.markdown(chat_bubble(reply, reply_time, "assistant"), unsafe_allow_html=True)