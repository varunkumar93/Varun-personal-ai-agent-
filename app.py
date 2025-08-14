import streamlit as st
import requests

st.set_page_config(page_title="Varun's AI Agent", layout="centered")
st.title("🤖 Varun's Personal AI Agent")
st.markdown("Ask me anything — coding, QA, mock interviews, productivity tips!")

user_input = st.text_input("💬 Your question:")

# Example chat data (replace with your own logic)
chat_data = [
    {
        "time": "13:39",
        "avatar": "https://cdn-icons-png.flaticon.com/512/847/847969.png",
        "message": "Hello 😊 How can I assist you today? 🚀"
    },
    {
        "time": "13:40",
        "avatar": "https://cdn-icons-png.flaticon.com/512/847/847969.png",
        "message": "Hi again 👋 What's up? How can I brighten your day today? 😊"
    }
]

# Display chat
for chat in chat_data:
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; margin-bottom:10px;">
            <img src="{chat['avatar']}" style="width:35px;height:35px;border-radius:50%;margin-right:8px;">
            <div>
                <div style="font-size:0.8em; color: gray;">{chat['time']}</div>
                <div style="background-color:#2c2c2c; padding:8px 12px; border-radius:8px; color:white;">
                    {chat['message']}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )