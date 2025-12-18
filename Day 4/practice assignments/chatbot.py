import streamlit as st
import requests
import os
from dotenv import load_dotenv

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="🤖 Groq vs LM Studio", layout="centered")
st.title("🤖 Chatbot")

# -------------------------
# LOAD ENV
# -------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# API URLs
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

# -------------------------
# SESSION STATE
# -------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.header("Options")
    model_choice = st.radio("Choose Model", ["Groq", "LM Studio"])
    show_history = st.checkbox("Show Chat History", value=True)

# -------------------------
# SHOW CHAT HISTORY
# -------------------------
if show_history:
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

# -------------------------
# FUNCTIONS
# -------------------------
def groq_response(messages):
    if not GROQ_API_KEY:
        return "❌ GROQ_API_KEY not found"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=20)
    except Exception as e:
        return f"❌ Groq Network Error: {e}"

    if response.status_code != 200:
        return f"❌ Groq API Error {response.status_code}: {response.text}"

    data = response.json()

    if "choices" not in data:
        return f"❌ Groq Invalid Response: {data}"

    return data["choices"][0]["message"]["content"]


def lm_studio_response(messages):
    payload = {
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=20)
    except Exception as e:
        return f"❌ LM Studio Connection Error: {e}"

    if response.status_code != 200:
        return f"❌ LM Studio Error {response.status_code}: {response.text}"

    data = response.json()

    if "choices" not in data:
        return f"❌ LM Studio Invalid Response: {data}"

    return data["choices"][0]["message"]["content"]

# -------------------------
# USER INPUT
# -------------------------
user_prompt = st.chat_input("Type your question...")

if user_prompt:
    # Store user message
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"Generating response from {model_choice}..."):
            if model_choice == "Groq":
                reply = groq_response(st.session_state.chat_history)
            else:
                reply = lm_studio_response(st.session_state.chat_history)

            st.write(reply)

    # Store assistant reply
    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply}
    )
