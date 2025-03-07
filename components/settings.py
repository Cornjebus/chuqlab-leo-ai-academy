import streamlit as st
import logging
from auth.user_db import UserDatabase

logger = logging.getLogger(__name__)

def display_settings():
    """Display user settings and preferences."""
    st.header("⚙️ Settings")
    
    # Check if user is authenticated
    if not st.session_state.get("authenticated", False):
        st.warning("Please log in to access settings.")
        return
    
    # Get username from session state
    username = st.session_state.get("username", "")
    if not username:
        st.error("User information not found. Please log out and log in again.")
        return
    
    # Create tabs for different settings sections
    tab1, tab2 = st.tabs(["Profile Settings", "Appearance"])
    
    # Profile settings tab
    with tab1:
        st.subheader("Profile Information")
        
        # Load user data
        user_db = UserDatabase()
        user_data = user_db.get_user_data(username)
        
        if not user_data:
            st.error("Could not load user data. Please try again later.")
            return
        
        # Create a form for profile info
        with st.form("profile_form"):
            name = st.text_input("Full Name", value=user_data.get("name", ""))
            email = st.text_input("Email Address", value=user_data.get("email", ""))
            
            # Password change fields
            st.markdown("---")
            st.subheader("Change Password")
            
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            # Submit button
            submitted = st.form_submit_button("Save Changes")
            
            if submitted:
                # Initialize status flags
                profile_updated = False
                password_updated = False
                
                # Update profile information if changed
                if name != user_data.get("name", "") or email != user_data.get("email", ""):
                    try:
                        # Create updated user data
                        updated_data = {
                            "name": name,
                            "email": email
                        }
                        
                        # Update user data in database (custom function needed)
                        if update_user_profile(username, updated_data):
                            st.success("Profile information updated successfully!")
                            profile_updated = True
                            
                            # Update session state
                            st.session_state.name = name
                        else:
                            st.error("Could not update profile information. Please try again.")
                    except Exception as e:
                        logger.error(f"Error updating profile: {str(e)}")
                        st.error(f"An error occurred: {str(e)}")
                
                # Update password if all fields are filled
                if current_password and new_password and confirm_password:
                    # Verify passwords match
                    if new_password != confirm_password:
                        st.error("New passwords do not match.")
                    elif len(new_password) < 6:
                        st.error("New password must be at least 6 characters long.")
                    else:
                        try:
                            # Verify current password
                            if user_db.verify_user(username, current_password):
                                # Update password functionality (add this to UserDatabase)
                                if update_user_password(username, new_password):
                                    st.success("Password updated successfully!")
                                    password_updated = True
                                else:
                                    st.error("Could not update password. Please try again.")
                            else:
                                st.error("Current password is incorrect.")
                        except Exception as e:
                            logger.error(f"Error updating password: {str(e)}")
                            st.error(f"An error occurred: {str(e)}")
        
        # Progress information
        st.subheader("Learning Progress")
        
        lesson_progress = user_data.get("lesson_progress", 0)
        st.info(f"You have completed {lesson_progress} lessons.")
        
        # Reset progress button with confirmation
        if st.button("Reset Learning Progress"):
            st.warning("Are you sure? This will reset all your lesson progress and quiz scores.")
            confirm_col1, confirm_col2 = st.columns(2)
            
            with confirm_col1:
                if st.button("Yes, Reset Everything", type="primary"):
                    try:
                        if reset_user_progress(username):
                            # Update session state
                            st.session_state.lesson_progress = 0
                            st.success("Progress has been reset successfully!")
                            st.rerun()
                        else:
                            st.error("Could not reset progress. Please try again.")
                    except Exception as e:
                        logger.error(f"Error resetting progress: {str(e)}")
                        st.error(f"An error occurred: {str(e)}")
            
            with confirm_col2:
                if st.button("Cancel"):
                    st.rerun()
    
    # Appearance settings tab
    with tab2:
        st.subheader("Display Preferences")
        
        # Theme preference
        st.write("Theme")
        theme_options = ["Light", "Dark", "System Default"]
        selected_theme = st.selectbox(
            "Choose theme", 
            options=theme_options,
            index=theme_options.index("System Default")
        )
        
        # Text size preference
        text_size = st.slider(
            "Text Size", 
            min_value=80, 
            max_value=120, 
            value=100, 
            step=10,
            format="%d%%"
        )
        
        # Code display preference
        code_theme = st.selectbox(
            "Code Block Theme",
            options=["Default", "Monokai", "GitHub", "VS Code"]
        )
        
        # Save button
        if st.button("Save Appearance Settings"):
            st.success("Appearance settings saved!")
            # In a real implementation, these would be saved to the user's profile

def update_user_profile(username, updated_data):
    """Update user profile in the database.
    
    Args:
        username (str): Username of the user to update
        updated_data (dict): New user data
        
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        # Load the user database
        user_db = UserDatabase()
        
        # Get current user data
        user_data = user_db.get_user_data(username)
        if not user_data:
            return False
        
        # Load the database
        db = user_db._load_db()
        if username not in db:
            return False
        
        # Update user data
        for key, value in updated_data.items():
            db[username][key] = value
        
        # Save the database
        user_db._save_db(db)
        
        return True
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        return False

def update_user_password(username, new_password):
    """Update user password in the database.
    
    Args:
        username (str): Username of the user to update
        new_password (str): New password
        
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        # Load the user database
        user_db = UserDatabase()
        
        # Get current user data
        user_data = user_db.get_user_data(username)
        if not user_data:
            return False
        
        # Load the database
        db = user_db._load_db()
        if username not in db:
            return False
        
        # Hash the new password
        import bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
        
        # Update password
        db[username]['password_hash'] = hashed_password.decode('utf-8')
        
        # Save the database
        user_db._save_db(db)
        
        return True
    except Exception as e:
        logger.error(f"Error updating user password: {str(e)}")
        return False

def reset_user_progress(username):
    """Reset user learning progress.
    
    Args:
        username (str): Username of the user to update
        
    Returns:
        bool: True if reset was successful, False otherwise
    """
    try:
        # Load the user database
        user_db = UserDatabase()
        
        # Load the database
        db = user_db._load_db()
        if username not in db:
            return False
        
        # Reset progress
        db[username]['lesson_progress'] = 0
        db[username]['completed_lessons'] = []
        db[username]['quiz_scores'] = {}
        
        # Save the database
        user_db._save_db(db)
        
        return True
    except Exception as e:
        logger.error(f"Error resetting user progress: {str(e)}")
        return False 