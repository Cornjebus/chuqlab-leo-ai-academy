import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import logging
from content.lesson_content import get_lesson, get_lesson_count, get_lesson_titles
from auth.user_db import UserDatabase

logger = logging.getLogger(__name__)

def display_lessons():
    """Display the lessons page with lesson navigation and content."""
    st.header("📚 Lessons")
    
    # Get current lesson ID from session state or default to 1
    if "current_lesson" not in st.session_state:
        st.session_state.current_lesson = 1
        
    # Get user progress info
    username = st.session_state.get("username", None)
    user_db = UserDatabase() if username else None
    
    # Set up container for the lesson
    lesson_container = st.container()
    
    # Get the current lesson content
    current_lesson_id = st.session_state.current_lesson
    lesson = get_lesson(current_lesson_id)
    
    # Get lesson count for navigation
    total_lessons = get_lesson_count()
    
    # Display lesson content
    with lesson_container:
        # If lesson not found
        if not lesson:
            st.warning(f"Lesson {current_lesson_id} not found")
            return
        
        # Display navigation bar and progress
        st.markdown(
            f"<div style='font-size: 0.8rem; color:#666;'>Lesson {current_lesson_id} of {total_lessons}</div>", 
            unsafe_allow_html=True
        )
        
        progress_value = (current_lesson_id - 1) / max(total_lessons - 1, 1)
        st.progress(progress_value)
        
        # Navigation buttons - placed at the top and bottom
        display_navigation_buttons(current_lesson_id, total_lessons, username, user_db, "top")
        
        # Display the actual lesson content
        display_lesson_content(current_lesson_id, username, user_db)
        
        # Show navigation buttons at bottom too
        st.markdown("---")
        display_navigation_buttons(current_lesson_id, total_lessons, username, user_db, "bottom")

def display_navigation_buttons(current_lesson_id, total_lessons, username, user_db, position="top"):
    """Display the lesson navigation buttons.
    
    Args:
        current_lesson_id: The current lesson ID
        total_lessons: The total number of lessons
        username: Current username
        user_db: UserDatabase instance
        position: Position identifier (top/bottom) to create unique keys
    """
    # Determine user progress for unlocking lessons
    user_progress = st.session_state.get("lesson_progress", 0)
    
    # Create columns for navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        # Previous lesson button (disabled for lesson 1)
        previous_disabled = current_lesson_id <= 1
        
        if previous_disabled:
            st.button("◀ Previous", disabled=True, key=f"prev_{position}_{current_lesson_id}")
        else:
            if st.button("◀ Previous", key=f"prev_{position}_{current_lesson_id}"):
                st.session_state.current_lesson = current_lesson_id - 1
                st.rerun()
    
    with col2:
        # Create a centered container for the "Next Lesson" button or completion info
        if username and user_db and current_lesson_id > user_progress:
            # This lesson is ahead of the user's progress - show completion button
            if st.button("Mark as Completed", use_container_width=True, key=f"complete_{position}_{current_lesson_id}"):
                # Update user progress
                user_db.update_lesson_progress(username, current_lesson_id)
                
                # Update session state
                st.session_state.lesson_progress = current_lesson_id
                
                # Log the progress update
                logger.info(f"User {username} completed lesson {current_lesson_id}")
                
                # Display success message
                st.success(f"Lesson {current_lesson_id} marked as completed!")
                
                # Go to the next lesson if available
                if current_lesson_id < total_lessons:
                    st.session_state.current_lesson = current_lesson_id + 1
                    st.rerun()
    
    with col3:
        # Next lesson button (disabled for last lesson or if next lesson is locked)
        next_disabled = (current_lesson_id >= total_lessons or 
                         (username and current_lesson_id > user_progress))
        
        # Special case: If this is the current progress lesson, allow going to the next one
        # even if it's not completed yet (previewing next lesson)
        if username and current_lesson_id == user_progress:
            next_disabled = False
        
        if next_disabled:
            st.button("Next ▶", disabled=True, key=f"next_{position}_{current_lesson_id}")
        else:
            if st.button("Next ▶", key=f"next_{position}_{current_lesson_id}"):
                # Log navigation
                logger.info(f"User {username} navigating from lesson {current_lesson_id} to {current_lesson_id + 1}")
                
                # Update session state with the next lesson
                st.session_state.current_lesson = current_lesson_id + 1
                
                # Rerun to show the new lesson
                st.rerun()

def display_lesson_content(lesson_id, username, user_db):
    """Display the content for a specific lesson."""
    # Get the lesson data
    lesson = get_lesson(lesson_id)
    if not lesson:
        st.warning(f"Lesson {lesson_id} not found")
        return
    
    try:
        # Display lesson title and description
        st.header(lesson['title'])
        st.subheader(lesson['description'])
        
        # Display lesson content sections
        content = lesson.get('content', {})
        
        # Handle different content structures
        if isinstance(content, str):
            # If content is just a string, display it directly
            st.markdown(content)
        elif isinstance(content, dict):
            # If content is a dictionary, display each section
            for section_title, section_content in content.items():
                st.markdown(f"## {section_title}")
                st.markdown(section_content)
        else:
            # Fallback for other content types
            st.warning("Lesson content format not supported")
        
        # Display lesson media if available
        if 'image_path' in lesson and lesson['image_path']:
            image_path = lesson['image_path']
            try:
                st.image(image_path, caption=f"Image for {lesson['title']}", use_container_width=True)
            except Exception as e:
                st.info(f"📸 Image placeholder for: {lesson['title']}\n\nThe image will be added soon!")
        
        if 'video_url' in lesson and lesson['video_url']:
            try:
                st.video(lesson['video_url'])
            except Exception as e:
                st.info("🎥 Video content will be available soon!")
        
        # Show estimated time to complete
        if 'time' in lesson:
            st.info(f"⏱️ Estimated time to complete: {lesson['time']} minutes")
        elif 'estimated_time' in lesson:
            st.info(f"⏱️ Estimated time to complete: {lesson['estimated_time']} minutes")
        
        # Quiz button at the end of the lesson
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1.5, 2, 1.5])
        
        with col2:
            if st.button("Take Quiz for This Lesson ✅", use_container_width=True, key=f"quiz_btn_{lesson_id}"):
                st.session_state.page = "Quizzes"
                st.session_state.current_quiz = lesson_id
                st.rerun()
    
    except Exception as e:
        logger.error(f"Error displaying lesson: {str(e)}")
        st.error(f"An error occurred while displaying the lesson: {str(e)}")
        if st.session_state.get("debug_mode", False):
            st.exception(e)