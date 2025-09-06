"""
Authentication module for user login, registration, and session management
"""

import streamlit as st
import hashlib
import secrets
from typing import Optional, Dict
from models import create_user, get_user_by_email, update_user

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hashed password"""
    return hash_password(password) == hashed_password

def generate_token() -> str:
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

def check_authentication() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def login_user(email: str, password: str) -> bool:
    """Login user with email and password"""
    try:
        user = get_user_by_email(email)
        if user and verify_password(password, user.get('password', '')):
            # Set session state
            st.session_state.authenticated = True
            st.session_state.user = {
                'id': user['_id'],
                'name': user['name'],
                'email': user['email'],
                'role': user.get('role', 'user'),
                'created_at': str(user.get('created_at', ''))
            }
            st.session_state.token = generate_token()
            return True
        return False
    except Exception as e:
        st.error(f"Login error: {e}")
        return False

def logout_user():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.token = None
    st.session_state.page = "home"
    st.session_state.selected_temple = None

def register_user(name: str, email: str, password: str, role: str = "user") -> bool:
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            return False
        
        # Create new user
        user_data = {
            'name': name,
            'email': email,
            'password': hash_password(password),
            'role': role
        }
        
        user_id = create_user(user_data)
        return user_id is not None
    except Exception as e:
        st.error(f"Registration error: {e}")
        return False

def update_user_password(user_id: str, old_password: str, new_password: str) -> bool:
    """Update user password"""
    try:
        # Verify old password first
        user = get_user_by_email(st.session_state.user['email'])
        if not user or not verify_password(old_password, user.get('password', '')):
            return False
        
        # Update password
        update_data = {
            'password': hash_password(new_password)
        }
        return update_user(user_id, update_data)
    except Exception as e:
        st.error(f"Password update error: {e}")
        return False

def require_auth(role: Optional[str] = None):
    """Decorator to require authentication for certain functions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not check_authentication():
                st.error("Please login to access this feature")
                st.session_state.page = "login"
                st.rerun()
            
            if role and st.session_state.user.get('role') != role:
                st.error(f"Access denied. {role.title()} privileges required.")
                st.session_state.page = "home"
                st.rerun()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def is_admin() -> bool:
    """Check if current user is admin"""
    return (check_authentication() and 
            st.session_state.user and 
            st.session_state.user.get('role') == 'admin')

def get_current_user() -> Optional[Dict]:
    """Get current authenticated user"""
    if check_authentication():
        return st.session_state.user
    return None

# Session management helpers
def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'selected_temple' not in st.session_state:
        st.session_state.selected_temple = None

def clear_session():
    """Clear all session data"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()
