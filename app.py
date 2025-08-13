import streamlit as st
import requests

st.set_page_config(page_title="Varun's AI Agent", layout="centered")
st.title("🤖 Varun's Personal AI Agent")
st.markdown("Ask me anything — coding, QA, mock interviews, productivity tips!")

user_input = st.text_input("💬 Your question:")

def get_response(prompt):
    headers = {
        "Authorization": f"Bearer {st.secrets['openrouter_key']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openrouter/llama2-13b-chat",
        "messages": [
            {"role": "system", "content": "You are Varun's helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

if user_input:
    with st.spinner("Thinking..."):
        try:
            output = get_response(user_input)
            st.success(output)
        except Exception as e:
            st.error(f"Error: {e}")
