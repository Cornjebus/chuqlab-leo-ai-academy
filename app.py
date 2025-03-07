import streamlit as st
import os
from dotenv import load_dotenv
import logging
from pathlib import Path
import datetime

# Import components
from auth.auth_handler import authenticate, logout
from auth.user_db import UserDatabase
from components.navigation import create_sidebar
from components.lessons import display_lessons
from components.quizzes import display_quiz
from components.playground import display_playground
from components.settings import display_settings
from components.debug import display_debug
from components.admin import display_admin
from utils.session_state import initialize_session_state

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# App configuration
st.set_page_config(
    page_title="Chuqlab LEO AI Academy",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
def apply_custom_css():
    st.markdown("""
    <style>
    /* Main header styling */
    .main-header {
        color: #1E3A8A;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    
    /* Subheader styling */
    .sub-header {
        color: #4A5568;
        font-size: 1.2rem;
        font-weight: 400;
        margin-top: 0;
        padding-top: 0;
        margin-bottom: 2rem;
    }
    
    /* Card styling for content sections */
    .stCard {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #718096;
        font-size: 0.8rem;
        margin-top: 5rem;
        padding: 1rem;
        border-top: 1px solid #E2E8F0;
    }
    
    /* Make DataFrames more compact */
    .dataframe-container th {
        font-size: 0.9rem;
        font-weight: 600;
        text-align: left;
    }
    
    .dataframe-container td {
        font-size: 0.9rem;
    }
    
    /* Improve button appearance */
    .stButton>button {
        border-radius: 5px;
        font-weight: 600;
    }
    
    /* Add space between sidebar items */
    .sidebar-item {
        margin-bottom: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
def add_footer():
    """Add a footer to the app"""
    footer_text = f"""
    <div class="footer">
        <p>Chuqlab LEO AI Academy | Developed for Law Enforcement Education | © {datetime.datetime.now().year}</p>
        <p>Version 1.0 | <a href="mailto:support@example.com">Contact Support</a></p>
    </div>
    """
    st.markdown(footer_text, unsafe_allow_html=True)

def main():
    """Main application function.
    
    Handles authentication and routing to different sections of the app.
    """
    try:
        # Apply custom CSS
        apply_custom_css()
        
        # Initialize session state for page navigation if not already set
        if "page" not in st.session_state:
            st.session_state.page = "Home"
        
        # Check if user is authenticated
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        
        # Authenticate user if not already authenticated
        if not st.session_state.authenticated:
            # Display login/registration form
            authenticate()
        else:
            # Create sidebar for authenticated users
            create_sidebar()
            
            # Add direct debug access in footer
            st.sidebar.markdown("---")
            if st.sidebar.button("🔍 Debug Tools"):
                st.session_state.page = "Debug"
                st.rerun()
            
            # Load user's lesson progress if not already loaded
            if "lesson_progress" not in st.session_state and "username" in st.session_state:
                user_db = UserDatabase()
                user_data = user_db.get_user_data(st.session_state.username)
                
                if user_data:
                    st.session_state.lesson_progress = user_data.get('lesson_progress', 0)
                    logger.info(f"Loaded progress for user {st.session_state.username}: {st.session_state.lesson_progress} lessons completed")
            
            # Display the selected page
            if st.session_state.page == "Home":
                display_home()
            elif st.session_state.page == "Lessons":
                display_lessons()
            elif st.session_state.page == "Quizzes":
                display_quiz()
            elif st.session_state.page == "Playground":
                display_playground()
            elif st.session_state.page == "Settings":
                display_settings()
            elif st.session_state.page == "Admin":
                display_admin()
            elif st.session_state.page == "Debug":
                display_debug()
        
        # Navigate to the selected page
        if st.session_state.get("page_changed", False):
            st.session_state.page_changed = False
            st.rerun()
        
        # Add footer
        add_footer()
            
    except Exception as e:
        logger.error(f"Error in main application: {str(e)}")
        st.error(f"An error occurred: {str(e)}")

def display_home():
    st.markdown('<h1 class="main-header">Welcome to Chuqlab LEO AI Academy</h1>', unsafe_allow_html=True)
    
    # Introduction section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Your Journey into AI and Large Language Models
        
        This platform is designed to help beginners understand AI concepts in a simple, 
        interactive way. Whether you're in law enforcement or just curious about AI, 
        this is the perfect place to start.
        
        ### What You'll Learn:
        
        - What AI and Large Language Models (LLMs) are
        - Basic concepts of machine learning
        - How to effectively communicate with AI systems
        - Practical applications of AI in various contexts
        - Ethical considerations for AI in law enforcement
        
        ### How to Use This Platform:
        
        1. **Lessons**: Start with structured lessons that introduce key concepts
        2. **Quizzes**: Test your understanding after each lesson
        3. **Playground**: Practice with real AI models and see your skills in action
        """)
    
    with col2:
        # Display a simple icon or image
        st.image("https://img.icons8.com/fluency/240/artificial-intelligence.png", width=200)
        
        # Quick navigation buttons
        st.subheader("Quick Start")
        if st.button("🚀 Begin First Lesson"):
            st.session_state.page = "Lessons"
            st.session_state.current_lesson = 1
            st.rerun()
            
        if st.button("🧠 Try the AI Playground"):
            st.session_state.page = "Playground"
            st.rerun()
    
    # Display progress if user has started lessons
    if st.session_state.get("lesson_progress"):
        st.subheader("Your Progress")
        progress = st.session_state.lesson_progress
        total_lessons = 6  # Updated to include our new lesson
        
        st.progress(progress / total_lessons)
        st.write(f"You've completed {progress} out of {total_lessons} lessons!")
        
        if progress > 0:
            last_completed = progress
            if st.button("Continue Learning"):
                st.session_state.page = "Lessons"
                # Set current lesson to the next uncompleted one
                st.session_state.current_lesson = min(last_completed + 1, total_lessons)
                st.rerun()
    
    # Featured content section
    st.markdown("---")
    st.subheader("Featured Content")
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown("### 🔍 What is AI?")
        st.markdown("Learn the fundamentals of artificial intelligence and machine learning.")
        if st.button("Explore Basics", key="basics"):
            st.session_state.page = "Lessons"
            st.session_state.current_lesson = 1
            st.rerun()
            
    with feat_col2:
        st.markdown("### 🤖 Prompting Skills")
        st.markdown("Master the art of effective communication with AI systems.")
        if st.button("Learn Prompting", key="prompting"):
            st.session_state.page = "Lessons"
            st.session_state.current_lesson = 4
            st.rerun()
            
    with feat_col3:
        st.markdown("### 🛡️ AI Ethics")
        st.markdown("Understand the ethical considerations of AI in law enforcement.")
        if st.button("Explore Ethics", key="ethics"):
            st.session_state.page = "Lessons"
            st.session_state.current_lesson = 6
            st.rerun()
        
if __name__ == "__main__":
    main() 