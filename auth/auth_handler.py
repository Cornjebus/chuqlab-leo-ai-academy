import streamlit as st
import streamlit_authenticator as stauth
import os
import firebase_admin
from firebase_admin import credentials, auth
import extra_streamlit_components as stx
from datetime import datetime, timedelta
import yaml
from yaml.loader import SafeLoader
import logging
import json
from auth.user_db import UserDatabase

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Firebase for authentication (if environment variables are set)
def init_firebase():
    if not firebase_admin._apps:
        try:
            # Check if a service account credentials file exists
            cred_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
            if cred_file and os.path.exists(cred_file):
                cred = credentials.Certificate(cred_file)
            else:
                # Use environment variables to create a temporary credentials file
                firebase_config = {
                    "type": "service_account",
                    "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
                    "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
                    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
                    "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL")
                }
                
                # Write to temporary file
                with open('firebase-credentials-temp.json', 'w') as f:
                    json.dump(firebase_config, f)
                
                cred = credentials.Certificate('firebase-credentials-temp.json')
                
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized successfully")
            
            # Clean up the temporary file
            if os.path.exists('firebase-credentials-temp.json'):
                os.remove('firebase-credentials-temp.json')
                
        except Exception as e:
            logger.error(f"Firebase initialization error: {e}")
            return False
    return True

# Function to load users from a YAML file (for development/testing)
def load_users():
    try:
        with open('users.yaml') as file:
            users = yaml.load(file, Loader=SafeLoader)
        return users
    except FileNotFoundError:
        # Create a default user file if it doesn't exist
        users = {
            'credentials': {
                'usernames': {
                    'admin': {
                        'email': 'admin@example.com',
                        'name': 'Admin User',
                        'password': stauth.Hasher(['admin']).generate()[0]
                    }
                }
            }
        }
        with open('users.yaml', 'w') as file:
            yaml.dump(users, file)
        return users

# Get cookie manager for session
def get_cookie_manager():
    cookie_manager = stx.CookieManager()
    return cookie_manager

# Main authentication function
def authenticate():
    """Handle user authentication.
    
    Displays login and registration forms and handles authentication logic.
    Updates session state with authentication status and user information.
    """
    # Apply authentication styles
    st.markdown("""
    <style>
    .auth-container {
        max-width: 500px;
        margin: 0 auto;
    }
    
    .auth-header {
        text-align: center;
        color: #1E3A8A;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
    }
    
    .auth-tabs {
        border-radius: 5px;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .form-group {
        margin-bottom: 1.2rem;
    }
    
    .auth-message {
        padding: 10px;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .auth-error {
        background-color: #FEE2E2;
        border: 1px solid #F87171;
        color: #B91C1C;
    }
    
    .auth-success {
        background-color: #D1FAE5;
        border: 1px solid #34D399;
        color: #047857;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Authentication container
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="auth-header">Welcome to Chuqlab LEO AI Academy</h2>', unsafe_allow_html=True)
    
    # Initialize session state variables for errors and success messages
    if "login_error" not in st.session_state:
        st.session_state.login_error = None
    
    if "register_error" not in st.session_state:
        st.session_state.register_error = None
        
    if "register_success" not in st.session_state:
        st.session_state.register_success = None
    
    # Create tabs for login and registration
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    # Handle demo login buttons (must be defined before forms)
    if "demo_user_clicked" not in st.session_state:
        st.session_state.demo_user_clicked = False
        
    if "demo_admin_clicked" not in st.session_state:
        st.session_state.demo_admin_clicked = False
    
    # Function to handle the demo user button click
    def demo_user_login():
        st.session_state.demo_user_clicked = True
    
    # Function to handle the demo admin button click
    def demo_admin_login():
        st.session_state.demo_admin_clicked = True
    
    with tab1:  # Login tab
        st.subheader("Login to Your Account")
        
        # Quick access with demo accounts - place OUTSIDE the form
        st.markdown("<p style='text-align: center; margin-top: 0.5rem;'>Demo accounts:</p>", unsafe_allow_html=True)
        demo_col1, demo_col2 = st.columns(2)
        
        # Demo user button
        with demo_col1:
            st.button("User Demo", use_container_width=True, key="demo_user_btn", on_click=demo_user_login)
        
        # Admin user button
        with demo_col2:
            st.button("Admin Demo", use_container_width=True, key="demo_admin_btn", on_click=demo_admin_login)
        
        # Handle demo login before the form
        if st.session_state.demo_user_clicked:
            st.session_state.demo_user_clicked = False  # Reset flag
            handle_login("demo", "demo123")
            
        if st.session_state.demo_admin_clicked:
            st.session_state.demo_admin_clicked = False  # Reset flag
            handle_login("admin", "admin123")
        
        # Login form
        with st.form("login_form"):
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            username = st.text_input("Username", key="login_username")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", key="login_password")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display error message if any
            if st.session_state.login_error:
                st.markdown(f'<div class="auth-message auth-error">{st.session_state.login_error}</div>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            # Handle form submission
            if submitted:
                handle_login(username, password)
    
    with tab2:  # Registration tab
        st.subheader("Create a New Account")
        
        # Registration form
        with st.form("registration_form"):
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            reg_username = st.text_input("Username", key="register_username")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            reg_name = st.text_input("Full Name", key="register_name")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            reg_email = st.text_input("Organization Email Address (required)", key="register_email")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            reg_agency = st.text_input("Organization Name (required)", key="register_agency")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            reg_password = st.text_input("Password", type="password", key="register_password")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            reg_password_confirm = st.text_input("Confirm Password", type="password", key="register_password_confirm")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add help text for email requirement
            st.markdown("""
            <div style='font-size: 0.8rem; color: #666; margin-bottom: 1rem;'>
                Note: Registration requires an organization email address. 
                Personal email addresses (Gmail, Yahoo, etc.) are not allowed.
            </div>
            """, unsafe_allow_html=True)
            
            # Display messages if any
            if st.session_state.register_error:
                st.markdown(f'<div class="auth-message auth-error">{st.session_state.register_error}</div>', unsafe_allow_html=True)
            
            if st.session_state.register_success:
                st.markdown(f'<div class="auth-message auth-success">{st.session_state.register_success}</div>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Register", type="primary", use_container_width=True)
            
            # Handle registration submission
            if submitted:
                handle_registration(reg_username, reg_password, reg_password_confirm, reg_name, reg_email, reg_agency)
    
    # Create demo accounts if they don't exist
    create_demo_accounts()
    
    st.markdown('</div>', unsafe_allow_html=True)

def handle_login(username, password):
    """Handle the login process."""
    if not username or not password:
        st.session_state.login_error = "Please enter both username and password"
    else:
        try:
            # Verify credentials
            user_db = UserDatabase()
            if user_db.verify_user(username, password):
                # Login successful
                user_data = user_db.get_user_data(username)
                
                # Update session state
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.name = user_data.get('name', username)
                
                # Load user progress
                st.session_state.lesson_progress = user_data.get('lesson_progress', 0)
                
                # Clear login error state
                st.session_state.login_error = None
                
                # Show success message and redirect
                st.success(f"Welcome back, {user_data.get('name', username)}!")
                st.rerun()
            else:
                st.session_state.login_error = "Invalid username or password"
        except Exception as e:
            logger.error(f"Login error: {e}")
            st.session_state.login_error = f"An error occurred during login: {str(e)}"

def handle_registration(username, password, password_confirm, name, email="", agency=""):
    """Handle the registration process."""
    # Validate inputs
    if not username or not password or not name or not email or not agency:
        st.session_state.register_error = "Please fill in all required fields"
        st.session_state.register_success = None
    elif password != password_confirm:
        st.session_state.register_error = "Passwords do not match"
        st.session_state.register_success = None
    elif len(password) < 6:
        st.session_state.register_error = "Password must be at least 6 characters long"
        st.session_state.register_success = None
    else:
        try:
            # Create new user
            user_db = UserDatabase()
            
            # Create the user with agency info
            success, error_msg = user_db.create_user(username, password, name, email, agency)
            
            if success:
                st.session_state.register_success = "Registration successful! You can now log in."
                st.session_state.register_error = None
            else:
                st.session_state.register_error = error_msg or "An error occurred during registration"
                st.session_state.register_success = None
        
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            st.session_state.register_error = f"An error occurred during registration: {str(e)}"
            st.session_state.register_success = None

def create_demo_accounts():
    """Create demo accounts if they don't exist."""
    try:
        user_db = UserDatabase()
        
        # Create demo user account
        if not user_db.user_exists("demo"):
            user_db.create_user(
                username="demo",
                password="demo123",
                name="Demo User",
                email="demo@example.com"
            )
            logger.info("Created demo user account")
        
        # Create admin account
        if not user_db.user_exists("admin"):
            user_db.create_user(
                username="admin",
                password="admin123",
                name="Admin User",
                email="admin@example.com"
            )
            logger.info("Created admin user account")
    
    except Exception as e:
        logger.error(f"Error creating demo accounts: {e}")

def logout():
    """Log out the current user."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun() 