import streamlit as st
import os
import logging
from auth.user_db import UserDatabase
from content.lesson_content import get_lesson_titles, get_lesson_count

logger = logging.getLogger(__name__)

def create_sidebar():
    """Create the sidebar navigation menu for the application.
    
    Returns:
        str: The name of the selected page
    """
    # Add logo/banner to sidebar
    st.sidebar.markdown("# Chuqlab LEO AI Academy")
    
    # Welcome message for authenticated users
    if st.session_state.get("authenticated", True):
        username = st.session_state.get("username", "Guest")
        name = st.session_state.get("name", username)
        st.sidebar.markdown(f"### Welcome, {name}!")
    
    # Debug mode toggle
    if "debug_mode" not in st.session_state:
        st.session_state.debug_mode = False
        
    debug_mode = st.session_state.debug_mode
    debug_toggle = st.sidebar.checkbox("Debug Mode", value=debug_mode)
    if debug_toggle != debug_mode:
        st.session_state.debug_mode = debug_toggle
        st.rerun()
    
    # Navigation menu
    st.sidebar.markdown("## Navigation")
    
    # Navigation options
    nav_options = {
        "Home": "🏠 Home",
        "Lessons": "📚 Lessons",
        "Quizzes": "✅ Quizzes",
        "Playground": "🚀 AI Playground"
    }
    
    # Add admin panel for admin users
    if st.session_state.get("username") == "admin":
        nav_options["Admin"] = "👤 Admin Panel"
    
    # Add debug page if in debug mode
    if st.session_state.debug_mode:
        nav_options["Debug"] = "🔍 Debug Tools"
    
    # Create navigation buttons
    for page_id, page_name in nav_options.items():
        # Highlight the current page
        is_current = st.session_state.page == page_id
        button_type = "primary" if is_current else "secondary"
        
        if st.sidebar.button(page_name, key=f"nav_{page_id}", type=button_type, use_container_width=True):
            # Store the current page before changing
            st.session_state.previous_page = st.session_state.page
            
            # Update the current page
            st.session_state.page = page_id
            
            # If going to lessons, set the current lesson to the user's progress
            if page_id == "Lessons" and "current_lesson" not in st.session_state:
                # Set current lesson to the user's progress or 1 if not set
                progress = st.session_state.get("lesson_progress", 0)
                # Progress is the last completed lesson, so view the next one
                st.session_state.current_lesson = max(1, progress + 1)
                logger.info(f"Setting current lesson to {st.session_state.current_lesson} based on progress {progress}")
            
            # If going to quizzes, set the current quiz to match the last viewed lesson
            if page_id == "Quizzes" and "current_quiz" not in st.session_state:
                if "current_lesson" in st.session_state:
                    st.session_state.current_quiz = st.session_state.current_lesson
            
            # Rerun to update the UI
            st.rerun()
    
    # If on lessons page, add lesson navigation
    if st.session_state.page == "Lessons":
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Lesson Navigation")
        
        # Get current lesson and total lesson count
        current_lesson = st.session_state.get("current_lesson", 1)
        total_lessons = get_lesson_count()
        
        # Determine the user's highest unlocked lesson (progress + 1)
        user_progress = st.session_state.get("lesson_progress", 0)
        highest_unlocked = min(total_lessons, max(1, user_progress + 1))
        
        # Get available lessons from 1 to highest_unlocked
        available_lessons = list(range(1, highest_unlocked + 1))
        
        # Get lesson titles
        lesson_titles = get_lesson_titles()
        
        # Format lesson options with titles
        lesson_options = [f"Lesson {i}: {lesson_titles.get(i, '')}" for i in available_lessons]
        
        # Find the index of current lesson in available lessons
        selected_index = available_lessons.index(current_lesson) if current_lesson in available_lessons else 0
        
        # Let user select a lesson
        selected_lesson = st.sidebar.selectbox(
            "Jump to Lesson", 
            options=available_lessons,
            format_func=lambda x: f"Lesson {x}: {lesson_titles.get(x, '')}", 
            index=selected_index
        )
        
        # Only navigate if a different lesson is selected
        if selected_lesson != current_lesson:
            st.session_state.current_lesson = selected_lesson
            logger.info(f"Navigating to lesson {selected_lesson}")
            st.rerun()
    
    # Add user progress information
    if st.session_state.get("authenticated", False):
        lesson_progress = st.session_state.get("lesson_progress", 0)
        
        st.sidebar.markdown("---")
        if lesson_progress > 0:
            st.sidebar.markdown(f"**Progress**: Completed {lesson_progress} lessons")
        else:
            st.sidebar.markdown("**Progress**: Just getting started!")
    
    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", type="secondary"):
        # Log the logout action
        logger.info(f"User {st.session_state.get('username', 'unknown')} logged out")
        
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        # Rerun to update UI
        st.rerun()
    
    st.sidebar.markdown('<div class="sidebar-footer">© 2025 AI Learning Platform</div>', unsafe_allow_html=True)
    
    # Return the current page
    return st.session_state.page 