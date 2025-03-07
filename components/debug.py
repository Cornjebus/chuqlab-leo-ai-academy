import streamlit as st
import json
import os
import yaml
from auth.user_db import UserDatabase

def display_debug():
    """Display a debug page with information about the current state of the application."""
    st.header("🔍 Debug Information")
    
    # Authentication status warning
    if not st.session_state.get("authenticated", False):
        st.warning("⚠️ You are not authenticated. Some features may not work correctly.")
    else:
        st.success(f"✅ Logged in as: {st.session_state.get('username', 'Unknown')}")
    
    # Session State
    st.subheader("Session State")
    
    # Filter out large objects like conversation history for cleaner display
    filtered_state = {}
    for key, value in st.session_state.items():
        if key == "conversation":
            filtered_state[key] = f"{len(value)} messages" if isinstance(value, list) else str(value)
        elif key == "prompt_templates":
            filtered_state[key] = f"{len(value)} templates" if isinstance(value, dict) else str(value)
        else:
            filtered_state[key] = value
    
    # Display current session state
    with st.expander("Current Session State", expanded=True):
        st.json(filtered_state)
    
    # User Database
    if st.session_state.get("authenticated", False):
        st.subheader("User Data")
        
        username = st.session_state.get("username", "")
        if username:
            user_db = UserDatabase()
            user_data = user_db.get_user_data(username)
            
            if user_data:
                # Remove sensitive information
                if "password_hash" in user_data:
                    user_data["password_hash"] = "[REDACTED]"
                    
                with st.expander("User Data from Database"):
                    st.json(user_data)
    
    # Navigation test utilities
    st.subheader("Navigation Tests")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Go to Lessons"):
            st.session_state.page = "Lessons"
            st.session_state.current_lesson = st.session_state.get("lesson_progress", 1)
            st.rerun()
    
    with col2:
        lesson_to_view = st.number_input("Lesson ID", min_value=1, max_value=10, value=1)
        if st.button("View Specific Lesson"):
            st.session_state.page = "Lessons"
            st.session_state.current_lesson = lesson_to_view
            st.rerun()
    
    with col3:
        if st.button("Go to Quizzes"):
            st.session_state.page = "Quizzes"
            st.rerun()
    
    # Reset options
    st.subheader("Reset Options")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset Navigation"):
            if "page" in st.session_state:
                del st.session_state.page
            if "current_lesson" in st.session_state:
                del st.session_state.current_lesson
            if "current_quiz" in st.session_state:
                del st.session_state.current_quiz
            st.success("Navigation state reset")
            st.rerun()
    
    with col2:
        if st.button("Reset Session State", type="primary"):
            for key in list(st.session_state.keys()):
                if key != "authenticated" and key != "username":
                    del st.session_state[key]
            st.warning("Session state has been reset (keeping authentication)")
            st.rerun()
    
    # File system information
    st.subheader("File System Information")
    
    if os.path.exists("users.yaml"):
        with st.expander("User Database File"):
            try:
                with open("users.yaml", "r") as f:
                    users_raw = yaml.safe_load(f)
                    
                    # Redact sensitive information
                    redacted_users = {}
                    for username, user_data in users_raw.items():
                        user_data_copy = user_data.copy()
                        if "password_hash" in user_data_copy:
                            user_data_copy["password_hash"] = "[REDACTED]"
                        redacted_users[username] = user_data_copy
                    
                    st.json(redacted_users)
            except Exception as e:
                st.error(f"Error reading users.yaml: {str(e)}")
    else:
        st.warning("users.yaml file not found")
    
    # Lesson progress debugging tool
    st.subheader("Fix Lesson Progress")
    
    if st.session_state.get("authenticated", False):
        username = st.session_state.get("username", "")
        if username:
            user_db = UserDatabase()
            current_progress = st.session_state.get("lesson_progress", 0)
            
            st.write(f"Current lesson progress: {current_progress}")
            
            new_progress = st.number_input("Set new lesson progress", 
                                          min_value=0, 
                                          max_value=10, 
                                          value=current_progress)
            
            if st.button("Update Progress"):
                user_db.update_lesson_progress(username, new_progress)
                st.session_state.lesson_progress = new_progress
                st.success(f"Lesson progress updated to {new_progress}")
                st.rerun()
    else:
        st.warning("Please log in to use this tool") 