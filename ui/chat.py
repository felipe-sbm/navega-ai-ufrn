import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def add_message(role, content):
    if role == "user":
        st.session_state.messages.append(HumanMessage(content=content))
    else:
        st.session_state.messages.append(AIMessage(content=content))

def display_chat_history():
    for message in st.session_state.messages:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)

def display_streaming_response(response_text):
    with st.chat_message("assistant"):
        st.markdown(response_text)
    return response_text

def clear_chat_history():
    st.session_state.messages = []
    if "current_response" in st.session_state:
        del st.session_state.current_response