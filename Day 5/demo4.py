'''from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)
conversation = [
    {"role": "system", "content": "You are a helpful assistant."}
]
while True:
    user_input = input("You:")
    if user_input == "exit":
        break
    user_msg = {"role": "user", "content": user_input}
    conversation.append(user_msg)
    llm_output = llm.invoke(conversation)
    print("AI:", llm_output.content)
    llm_msg = {"role": "assistant", "content":  llm_output.content}
    conversation.append(llm_msg)
'''
# Use slider value to decide how many last messages to be sent to LLM
# instead of full conversation. This will limit the "context length".

import streamlit as st
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv


load_dotenv()

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]


with st.sidebar:
    st.header("Settings")

    count = st.slider(
        "Message Count (Last N messages)",
        min_value=2,
        max_value=20,
        value=6,
        step=2
    )

    st.subheader("Config")
    st.json({"message_window": count})


st.title("Fan Chatbot 🤖 ")

# Show ONLY last N messages (like first app)
display_messages = st.session_state.messages[-count:]

for msg in display_messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])


user_input = st.chat_input("Say something...")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Context window for LLM
    context_to_send = st.session_state.messages[-count:]

    # Call LLM
    response = llm.invoke(context_to_send)

    # Add assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response.content}
    )

    # Refresh UI
    st.rerun()
