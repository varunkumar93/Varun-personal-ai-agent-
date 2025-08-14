import streamlit as st

st.set_page_config(page_title="Varun's AI Agent", layout="centered")
st.title("🤖 Varun's Personal AI Agent")
st.markdown("Ask me anything — coding, QA, mock interviews, productivity tips!")

user_input = st.text_input("💬 Your question:")

# Example chat data
chat_data = [
    {
        "time": "13:39",
        "role": "bot",
        "avatar": "https://cdn-icons-png.flaticon.com/512/847/847969.png",
        "message": "**Hello 😊** How can I assist you today? 🚀"
    },
    {
        "time": "13:40",
        "role": "user",
        "avatar": "https://cdn-icons-png.flaticon.com/512/847/847969.png",
        "message": "Hi again 👋 _What's up?_ How can I brighten your day today? 😊"
    },
    {
        "time": "13:41",
        "role": "bot",
        "avatar": "https://cdn-icons-png.flaticon.com/512/847/847969.png",
        "message": "Here’s a [Google link](https://google.com) you might find useful."
    }
]

# Display chat
for chat in chat_data:
    # Convert markdown to HTML using Streamlit, capture as string
    rendered_message = st._repr_html_(chat["message"]) if hasattr(st, "_repr_html_") else chat["message"]

    if chat["role"] == "bot":
        # Bot message - left
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                <img src="{chat['avatar']}" style="width:35px;height:35px;border-radius:50%;margin-right:8px;">
                <div style="background-color:#2c2c2c; padding:8px 12px; border-radius:8px; color:white; max-width: 80%;">
                    <div>{chat['message']}</div>
                    <div style="font-size:0.7em; color:gray; text-align:right; margin-top:3px;">{chat['time']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # User message - right
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; justify-content:flex-end; margin-bottom:10px;">
                <div style="background-color:#0066cc; padding:8px 12px; border-radius:8px; color:white; max-width: 80%;">
                    <div>{chat['message']}</div>
                    <div style="font-size:0.7em; color:lightgray; text-align:right; margin-top:3px;">{chat['time']}</div>
                </div>
                <img src="{chat['avatar']}" style="width:35px;height:35px;border-radius:50%;margin-left:8px;">
            </div>
            """,
            unsafe_allow_html=True
        )