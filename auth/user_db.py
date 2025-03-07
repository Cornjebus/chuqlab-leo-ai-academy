import os
import yaml
import logging
import datetime
import time
import bcrypt
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class UserDatabase:
    """User database handler using YAML file storage for simplicity.
    
    In a production environment, this would be replaced with a proper database.
    """
    
    def __init__(self, db_path='users.yaml'):
        """Initialize the user database.
        
        Args:
            db_path (str): Path to the YAML file storing user data
        """
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create the database file if it doesn't exist."""
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                yaml.dump({}, f)
            logger.info(f"Created new user database at {self.db_path}")
    
    def _load_db(self):
        """Load the user database from file.
        
        Returns:
            dict: User database
        """
        try:
            with open(self.db_path, 'r') as f:
                db = yaml.safe_load(f) or {}
            return db
        except Exception as e:
            logger.error(f"Error loading user database: {e}")
            return {}
    
    def _save_db(self, db):
        """Save the user database to file.
        
        Args:
            db (dict): User database to save
        """
        try:
            with open(self.db_path, 'w') as f:
                yaml.dump(db, f)
        except Exception as e:
            logger.error(f"Error saving user database: {e}")
    
    def user_exists(self, username):
        """Check if a user exists in the database.
        
        Args:
            username (str): Username to check
            
        Returns:
            bool: True if user exists, False otherwise
        """
        db = self._load_db()
        return username in db
    
    def is_law_enforcement_email(self, email):
        """Check if the email is from an organization (non-public email provider).
        
        Args:
            email (str): Email address to check
            
        Returns:
            bool: True if email is from an organization domain, False otherwise
        """
        if not email:
            return False
        
        # List of common public email domains to exclude
        public_email_domains = [
            '@gmail.',
            '@yahoo.',
            '@hotmail.',
            '@outlook.',
            '@aol.',
            '@icloud.',
            '@proton.',
            '@mail.',
            '@zoho.',
            '@yandex.',
            '@live.',
            '@msn.'
        ]
        
        email = email.lower()
        
        # Check if email contains any public domain
        for domain in public_email_domains:
            if domain in email:
                return False
        
        # Must have @ and . to be valid
        return '@' in email and '.' in email
    
    def create_user(self, username, password, name="", email="", agency=""):
        """Create a new user in the database.
        
        Args:
            username (str): Username for the new user
            password (str): Password for the new user
            name (str, optional): Full name of the user
            email (str, required): Email address of the user
            agency (str, optional): Organization name
            
        Returns:
            bool: True if user creation was successful, False otherwise
            str: Error message if creation failed, empty string if successful
        """
        try:
            # Validate required fields
            if not email:
                return False, "Email address is required"
            
            # Validate email format
            if not '@' in email or not '.' in email:
                return False, "Invalid email format"
            
            # Validate organization email
            if not self.is_law_enforcement_email(email):
                return False, "Registration is restricted to organization email addresses. Personal email providers (Gmail, Yahoo, etc.) are not allowed"
            
            db = self._load_db()
            
            # Check if user already exists
            if username in db:
                logger.warning(f"User {username} already exists")
                return False, "Username already exists"
            
            # Hash the password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Create user
            db[username] = {
                'username': username,
                'password_hash': hashed_password.decode('utf-8'),
                'name': name,
                'email': email,
                'agency': agency,
                'created_at': datetime.datetime.now().isoformat(),
                'lesson_progress': 0,
                'completed_lessons': [],
                'quiz_scores': {},
                'saved_conversations': []
            }
            
            self._save_db(db)
            logger.info(f"Created new user: {username}")
            return True, ""
        
        except Exception as e:
            logger.error(f"Error creating user {username}: {e}")
            return False, str(e)
    
    def verify_user(self, username, password):
        """Verify a user's login credentials.
        
        Args:
            username (str): Username to verify
            password (str): Password to verify
            
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        try:
            db = self._load_db()
            
            # Check if user exists
            if username not in db:
                logger.warning(f"User {username} not found")
                return False
            
            # Verify password
            stored_hash = db[username]['password_hash'].encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        
        except Exception as e:
            logger.error(f"Error verifying user {username}: {e}")
            return False
    
    def get_user_data(self, username):
        """Get data for a specific user.
        
        Args:
            username (str): Username to get data for
            
        Returns:
            dict: User data or None if user doesn't exist
        """
        db = self._load_db()
        return db.get(username, None)
    
    def update_lesson_progress(self, username, lesson_id):
        """Update a user's lesson progress.
        
        Args:
            username (str): Username to update
            lesson_id (int): ID of the completed lesson
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            db = self._load_db()
            
            # Check if user exists
            if username not in db:
                logger.warning(f"User {username} not found")
                return False
            
            # Update lesson progress
            current_progress = db[username].get('lesson_progress', 0)
            
            # Only update if this is higher than the current progress
            if lesson_id > current_progress:
                db[username]['lesson_progress'] = lesson_id
            
            # Add to completed lessons if not already there
            if 'completed_lessons' not in db[username]:
                db[username]['completed_lessons'] = []
                
            if lesson_id not in db[username]['completed_lessons']:
                db[username]['completed_lessons'].append(lesson_id)
            
            self._save_db(db)
            logger.info(f"Updated lesson progress for user {username}: completed lesson {lesson_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error updating lesson progress for user {username}: {e}")
            return False
    
    def update_quiz_score(self, username, quiz_id, score, answers=None):
        """Update a user's quiz score.
        
        Args:
            username (str): Username to update
            quiz_id (int): ID of the quiz
            score (float): Quiz score (percentage)
            answers (dict, optional): User's answers to quiz questions
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            db = self._load_db()
            
            # Check if user exists
            if username not in db:
                logger.warning(f"User {username} not found")
                return False
            
            # Initialize quiz scores if needed
            if 'quiz_scores' not in db[username]:
                db[username]['quiz_scores'] = {}
            
            # Convert quiz_id to string for YAML storage
            quiz_id_str = str(quiz_id)
            
            # Update quiz score
            # Only overwrite if new score is higher
            current_score = db[username]['quiz_scores'].get(quiz_id_str, {}).get('score', 0)
            if score >= current_score:
                db[username]['quiz_scores'][quiz_id_str] = {
                    'score': score,
                    'timestamp': datetime.datetime.now().isoformat(),
                    'answers': answers or {}
                }
            
            self._save_db(db)
            logger.info(f"Updated quiz score for user {username}: quiz {quiz_id}, score {score}%")
            return True
        
        except Exception as e:
            logger.error(f"Error updating quiz score for user {username}: {e}")
            return False
    
    def save_quiz_score(self, username, quiz_id, score, answers=None):
        """Save a user's quiz score (alias for update_quiz_score).
        
        Args:
            username (str): Username to update
            quiz_id (int or str): ID of the quiz
            score (float): Quiz score (percentage)
            answers (dict, optional): User's answers to quiz questions
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        return self.update_quiz_score(username, quiz_id, score, answers)
    
    def save_conversation(self, username, title, messages):
        """Save a user's playground conversation.
        
        Args:
            username (str): Username to update
            title (str): Title of the conversation
            messages (list): List of message objects from the conversation
            
        Returns:
            str: ID of the saved conversation, or False if saving failed
        """
        try:
            db = self._load_db()
            
            # Check if user exists
            if username not in db:
                logger.warning(f"User {username} not found")
                return False
            
            # Initialize saved conversations if needed
            if 'saved_conversations' not in db[username]:
                db[username]['saved_conversations'] = []
            
            # Generate a unique ID based on timestamp
            conversation_id = str(int(time.time()))
            
            # Create the conversation entry
            conversation = {
                'id': conversation_id,
                'title': title,
                'timestamp': datetime.datetime.now().isoformat(),
                'messages': messages
            }
            
            # Save conversation to separate file to avoid large YAML database
            conversations_dir = Path("conversations")
            conversations_dir.mkdir(exist_ok=True)
            
            conversation_file = conversations_dir / f"conversation-{username}-{conversation_id}.json"
            with open(conversation_file, 'w') as f:
                json.dump(conversation, f)
            
            # Add reference to user data
            db[username]['saved_conversations'].append({
                'id': conversation_id,
                'title': title,
                'timestamp': datetime.datetime.now().isoformat(),
                'file_path': str(conversation_file)
            })
            
            self._save_db(db)
            logger.info(f"Saved conversation for user {username}: {title} ({conversation_id})")
            return conversation_id
        
        except Exception as e:
            logger.error(f"Error saving conversation for user {username}: {e}")
            return False
    
    def get_conversation(self, username, conversation_id):
        """Get a saved conversation for a user.
        
        Args:
            username (str): Username to get conversation for
            conversation_id (str): ID of the conversation to retrieve
            
        Returns:
            dict: Conversation data or None if not found
        """
        try:
            db = self._load_db()
            
            # Check if user exists
            if username not in db:
                logger.warning(f"User {username} not found")
                return None
            
            # Find the conversation reference
            conversation_refs = db[username].get('saved_conversations', [])
            conversation_ref = next((c for c in conversation_refs if c['id'] == conversation_id), None)
            
            if not conversation_ref:
                logger.warning(f"Conversation {conversation_id} not found for user {username}")
                return None
            
            # Load from separate file
            file_path = conversation_ref.get('file_path')
            if file_path and os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            
            return None
        
        except Exception as e:
            logger.error(f"Error retrieving conversation for user {username}: {e}")
            return None
    
    def delete_conversation(self, username, conversation_id):
        """Delete a saved conversation for a user.
        
        Args:
            username (str): Username to delete conversation for
            conversation_id (str): ID of the conversation to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            db = self._load_db()
            
            # Check if user exists
            if username not in db:
                logger.warning(f"User {username} not found")
                return False
            
            # Find the conversation reference
            conversation_refs = db[username].get('saved_conversations', [])
            conversation_ref = next((c for c in conversation_refs if c['id'] == conversation_id), None)
            
            if not conversation_ref:
                logger.warning(f"Conversation {conversation_id} not found for user {username}")
                return False
            
            # Delete the separate file
            file_path = conversation_ref.get('file_path')
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            
            # Remove from user data
            db[username]['saved_conversations'] = [
                c for c in conversation_refs if c['id'] != conversation_id
            ]
            
            self._save_db(db)
            logger.info(f"Deleted conversation for user {username}: {conversation_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting conversation for user {username}: {e}")
            return False
    
    def delete_user(self, username):
        """Delete a user from the database.
        
        Args:
            username (str): Username of the user to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            db = self._load_db()
            
            # Check if user exists
            if username not in db:
                logger.warning(f"User {username} not found")
                return False
            
            # Don't allow deleting the admin user
            if username == "admin":
                logger.warning("Cannot delete admin user")
                return False
            
            # Delete user's saved conversations
            conversations_dir = Path("conversations")
            if conversations_dir.exists():
                for file in conversations_dir.glob(f"conversation-{username}-*.json"):
                    try:
                        file.unlink()
                    except Exception as e:
                        logger.error(f"Error deleting conversation file {file}: {e}")
            
            # Delete user from database
            del db[username]
            self._save_db(db)
            
            logger.info(f"Deleted user: {username}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting user {username}: {e}")
            return False 