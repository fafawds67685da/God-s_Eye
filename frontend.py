import streamlit as st
import requests
import time

st.set_page_config(page_title="God's Eye", layout="wide")
st.title("🤖 Real-Time AI Agent which can see !+"
"")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Say something to the agent...")
if prompt:
    st.chat_message("user").write(prompt)
    payload = {
        "user_input": prompt
    }
    try:
        res = requests.post("http://127.0.0.1:5001/chat", json=payload)
        response = res.json()
        reply = response.get("response")
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        message_placeholder = st.chat_message("assistant").empty()

        full_message = ""
        for ch in reply:
            full_message += ch
            message_placeholder.write(full_message)
            time.sleep(0.02)  # Small delay for typing effect
    except Exception as e:
        st.error("Failed to communicate with the agent. Please ensure the backend is running.")
