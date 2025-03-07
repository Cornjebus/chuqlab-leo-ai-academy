import streamlit as st
import logging
from auth.user_db import UserDatabase

logger = logging.getLogger(__name__)

def display_admin():
    """Display the admin panel with user management features."""
    st.header("👤 Admin Panel")
    
    # Check if user is authenticated and is admin
    if not st.session_state.get("authenticated", False):
        st.warning("Please log in to access the admin panel.")
        return
        
    username = st.session_state.get("username", "")
    if username != "admin":
        st.error("You do not have permission to access the admin panel.")
        return
    
    # Initialize user database
    user_db = UserDatabase()
    
    # Display registered users
    st.subheader("Registered Users")
    
    # Get all users
    db = user_db._load_db()
    
    # Create a table of users
    user_data = []
    for username, data in db.items():
        user_data.append({
            "Username": username,
            "Name": data.get("name", ""),
            "Email": data.get("email", ""),
            "Agency": data.get("agency", "Not specified"),
            "Lesson Progress": data.get("lesson_progress", 0),
            "Registration Date": data.get("created_at", "Unknown")
        })
    
    if user_data:
        st.dataframe(
            user_data,
            column_config={
                "Username": st.column_config.TextColumn("Username"),
                "Name": st.column_config.TextColumn("Full Name"),
                "Email": st.column_config.TextColumn("Email"),
                "Agency": st.column_config.TextColumn("Law Enforcement Agency"),
                "Lesson Progress": st.column_config.NumberColumn("Lesson Progress"),
                "Registration Date": st.column_config.DatetimeColumn("Registration Date")
            },
            hide_index=True
        )
    else:
        st.info("No registered users found.")
    
    # User Statistics
    st.subheader("User Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", len(user_data))
    
    with col2:
        active_users = sum(1 for user in user_data if user["Lesson Progress"] > 0)
        st.metric("Active Users", active_users)
    
    with col3:
        completed_users = sum(1 for user in user_data if user["Lesson Progress"] >= 8)
        st.metric("Completed Course", completed_users)
    
    # User Management
    st.subheader("User Management")
    
    # User deletion
    with st.expander("Delete User"):
        user_to_delete = st.selectbox(
            "Select user to delete:",
            [user["Username"] for user in user_data if user["Username"] != "admin"],
            key="user_to_delete"
        )
        
        if st.button("Delete User", key="delete_user_btn", type="primary"):
            if user_to_delete:
                # Add user deletion logic to UserDatabase class
                if hasattr(user_db, 'delete_user') and user_db.delete_user(user_to_delete):
                    st.success(f"User {user_to_delete} has been deleted.")
                    st.rerun()
                else:
                    st.error("Failed to delete user. Please try again.")
    
    # Export user data
    with st.expander("Export User Data"):
        if st.button("Download User Data (CSV)", key="export_users_btn"):
            # Create CSV from user_data
            import pandas as pd
            df = pd.DataFrame(user_data)
            csv = df.to_csv(index=False)
            
            st.download_button(
                "Click to Download",
                csv,
                "user_data.csv",
                "text/csv",
                key="download_users_csv"
            ) 