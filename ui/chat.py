import streamlit as st

def show_message(role, content):
    st.chat_message(role).write(content)