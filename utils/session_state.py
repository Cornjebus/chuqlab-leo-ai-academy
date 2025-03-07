import streamlit as st
import logging
from auth.user_db import UserDatabase

logger = logging.getLogger(__name__)

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    # Initialize navigation state
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    
    # Initialize lesson state
    if "current_lesson" not in st.session_state:
        st.session_state.current_lesson = 1
    
    # Initialize quiz state
    if "current_quiz" not in st.session_state:
        st.session_state.current_quiz = 1
    
    # Initialize quiz submission state
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    
    # Initialize playground state
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    # Load user data if authenticated
    if st.session_state.get("authenticated", False) and st.session_state.get("username"):
        load_user_progress(st.session_state.username)

def load_user_progress(username):
    """Load user progress from the database and update session state."""
    try:
        user_db = UserDatabase()
        user_data = user_db.get_user_data(username)
        
        if user_data:
            # Load lesson progress
            lesson_progress = user_data.get('lesson_progress', 0)
            st.session_state.lesson_progress = lesson_progress
            
            # Load completed quizzes and scores
            quiz_scores = user_data.get('quiz_scores', {})
            st.session_state.quiz_scores = quiz_scores
            
            # Load any saved playground conversations
            saved_conversations = user_data.get('saved_conversations', [])
            if saved_conversations and "conversation_history" not in st.session_state:
                st.session_state.saved_conversations = saved_conversations
                
            logger.info(f"Loaded progress for user {username}: {lesson_progress} lessons completed")
        else:
            # Initialize for new user
            st.session_state.lesson_progress = 0
            st.session_state.quiz_scores = {}
            logger.info(f"Initialized new progress for user {username}")
    
    except Exception as e:
        logger.error(f"Error loading user progress: {e}")
        st.session_state.lesson_progress = 0
        st.session_state.quiz_scores = {}

def update_user_progress(username, lesson_id):
    """Update user's lesson progress in both database and session state."""
    try:
        if not username:
            logger.warning("Cannot update progress: No username provided")
            return False
            
        # Update in database
        user_db = UserDatabase()
        current_progress = st.session_state.get("lesson_progress", 0)
        
        # Only update if this is a new highest lesson
        if lesson_id > current_progress:
            user_db.update_lesson_progress(username, lesson_id)
            
            # Update session state
            st.session_state.lesson_progress = lesson_id
            logger.info(f"Updated progress for user {username} to lesson {lesson_id}")
            return True
            
        return False
    
    except Exception as e:
        logger.error(f"Error updating user progress: {e}")
        return False

def update_quiz_score(username, quiz_id, score, answers=None):
    """Update user's quiz score in both database and session state."""
    try:
        if not username:
            logger.warning("Cannot update quiz score: No username provided")
            return False
            
        # Update in database
        user_db = UserDatabase()
        success = user_db.update_quiz_score(username, quiz_id, score, answers)
        
        if success:
            # Update session state
            if "quiz_scores" not in st.session_state:
                st.session_state.quiz_scores = {}
                
            st.session_state.quiz_scores[str(quiz_id)] = {
                "score": score,
                "answers": answers or {}
            }
            
            logger.info(f"Updated quiz {quiz_id} score for user {username}: {score}%")
            return True
            
        return False
    
    except Exception as e:
        logger.error(f"Error updating quiz score: {e}")
        return False

def save_conversation(username, title, messages):
    """Save the current playground conversation to user data."""
    try:
        if not username:
            logger.warning("Cannot save conversation: No username provided")
            return False
            
        # Update in database
        user_db = UserDatabase()
        conversation_id = user_db.save_conversation(username, title, messages)
        
        if conversation_id:
            # Update session state if needed
            if "saved_conversations" not in st.session_state:
                st.session_state.saved_conversations = []
                
            st.session_state.saved_conversations.append({
                "id": conversation_id,
                "title": title,
                "timestamp": str(conversation_id)  # Using ID as timestamp for simplicity
            })
            
            logger.info(f"Saved conversation '{title}' for user {username}")
            return conversation_id
            
        return False
    
    except Exception as e:
        logger.error(f"Error saving conversation: {e}")
        return False

def get_session_state():
    """Get all current session state variables"""
    return {key: value for key, value in st.session_state.items()} 