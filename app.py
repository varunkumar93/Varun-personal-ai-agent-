import streamlit as st
from datetime import datetime

# Page setup
st.set_page_config(page_title="Varun's AI Agent", layout="centered")
st.title("🤖 Varun's Personal AI Agent")

# Initialize chat history in session state
if "chat_data" not in st.session_state:
    st.session_state.chat_data = [
        {
            "time": datetime.now().strftime("%H:%M"),
            "avatar": "https://cdn-icons-png.flaticon.com/512/847/847969.png",
            "message": "Hello 😊 How can I assist you today? 🚀",
            "is_user": False
        }
    ]

# Function to display chat bubbles
def display_chat():
    for chat in st.session_state.chat_data:
        bubble_color = "#2c2c2c" if not chat["is_user"] else "#0078FF"
        align = "flex-start" if not chat["is_user"] else "flex-end"
        text_align = "left" if not chat["is_user"] else "right"

        st.markdown(
            f"""
            <div style="display:flex; justify-content:{align}; margin-bottom:10px;">
                <div style="max-width:70%; background-color:{bubble_color}; padding:8px 12px;
                            border-radius:10px; color:white; box-shadow:0px 2px 6px rgba(0,0,0,0.2); text-align:{text_align};">
                    {chat['message']}
                    <div style="font-size:0.7em; color:lightgray; margin-top:2px; text-align:{text_align};">
                        {chat['time']}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Show chat
display_chat()

# User input
user_input = st.text_input("💬 Your message:", key="input_box")

# On send
if user_input:
    st.session_state.chat_data.append({
        "time": datetime.now().strftime("%H:%M"),
        "avatar": "",
        "message": user_input,
        "is_user": True
    })

    # Example bot reply (replace with API call)
    st.session_state.chat_data.append({
        "time": datetime.now().strftime("%H:%M"),
        "avatar": "https://cdn-icons-png.flaticon.com/512/847/847969.png",
        "message": f"You said: {user_input}",
        "is_user": False
    })

    # Clear the input box after sending
    st.session_state.input_box = ""

    # Refresh page to show the new messages
    st.experimental_rerun()