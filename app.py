import streamlit as st
from assistant import get_chatbot

# Initialize chatbot
init_chat, chat_with_user, summarize_conversation = get_chatbot()

st.title("LexAI - Your Legal Assistant")

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = init_chat()

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])
    elif msg["role"] == "user":
        st.chat_message("user").write(msg["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    # Display user message
    st.chat_message("user").write(prompt)
    
    # Get and display assistant response
    response, st.session_state.messages = chat_with_user(st.session_state.messages, prompt)
    st.chat_message("assistant").write(response)