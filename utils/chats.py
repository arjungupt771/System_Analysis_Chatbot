import uuid
import streamlit as st             
from datetime import datetime
from utils.model import model
from chat_db import  save_message

def create_new_chat():
    chat_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.all_chats[chat_id]={
        "id": chat_id,
        "title": f"Chat - {timestamp}",
        "messages": [],
        "pdf_texts_associated":[],
        "created_at": timestamp
    }
    st.session_state.current_chat_id = chat_id
    st.session_state.gemini_chat_sessions[chat_id] = model.start_chat(history=[])
    st.rerun()
    
def select_chat(chat_id):
    st.session_state.current_chat_id = chat_id
    if chat_id not in st.session_state.gemini_chat_sessions:
        history_for_session = [
            {"role": msg["role"], "parts": msg["parts"]}
            for msg in st.session_state.all_chats[chat_id]["messages"]
        ]
        st.session_state.gemini_chat_sessions[chat_id] = model.start_chat(history = history_for_session)
    st.rerun()
    
def get_current_chat_data():
    if st.session_state.current_chat_id and st.session_state.current_chat_id in st.session_state.all_chats:
        return st.session_state.all_chats[st.session_state.current_chat_id]
    return None

def get_current_gemini_session():
    if st.session_state.current_chat_id and st.session_state.current_chat_id in st.session_state.gemini_chat_sessions:
        return st.session_state.gemini_chat_sessions[st.session_state.current_chat_id]
    return None

def add_message_to_current_chat(role, content):
    current_chat = get_current_chat_data()
    if current_chat:
        current_chat["messages"].append({"role":role, "parts": [content]})
        save_message(current_chat["id"], role, content)
        if role == "user" and len(current_chat["messages"]) == 1 and current_chat["title"].startswith("Chat - "):
            current_chat["title"] = content[:30] + "..."