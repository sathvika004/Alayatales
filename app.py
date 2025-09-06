"""
Alayatales - Temple Management System
A Streamlit application for managing temple information
"""

__version__ = "0.1.0"

import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv

# Import custom modules
from models import (
    init_database
)
from auth import (
    login_user,
    logout_user,
    register_user
)
from temple_pages import (
    show_home_page,
    show_temple_detail,
    show_add_temple,
    show_edit_temple,
    show_admin_dashboard,
    show_temple_list
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Alayatales",
    page_icon="🛕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database connection
db = init_database()
if db is None:
    st.warning("⚠️ Unable to connect to database.")
    mongodb_uri = os.getenv('MONGODB_URI', '')
    if 'mongodb+srv' in mongodb_uri:
        st.info("Please check your MongoDB Atlas connection and credentials.")
    else:
        st.info("Please install and start MongoDB to use all features.")
        st.code("./install-mongodb.sh  # For installation help", language="bash")

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main content area */
    .main {
        padding: 1rem;
    }
    
    /* Temple card styling */
    .temple-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Navigation styling */
    .nav-link {
        text-decoration: none;
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    
    .nav-link:hover {
        background-color: #e9ecef;
    }
    
    /* Image gallery styling */
    .image-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .gallery-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 5px;
    }
    
    /* Header styling */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: background-color 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'selected_temple' not in st.session_state:
    st.session_state.selected_temple = None

def show_header():
    """Display the application header with navigation"""
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        st.markdown("<h1 style='color: white; margin: 0;'>🛕 Alayatales</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: white; margin: 0;'>Discover Sacred Temples</p>", unsafe_allow_html=True)
    
    with col3:
        if st.session_state.authenticated:
            st.markdown(f"<p style='color: white; text-align: right;'>Welcome, {st.session_state.user['name']}!</p>", unsafe_allow_html=True)
            if st.button("Logout", key="logout_header"):
                logout_user()
                st.rerun()

def show_navigation():
    """Display navigation menu"""
    with st.sidebar:
        st.markdown("### Navigation")
        
        # Public menu items
        public_menu = ["🏠 Home", "🛕 All Temples"]
        
        # Admin menu items
        admin_menu = []
        if st.session_state.authenticated and st.session_state.user.get('role') == 'admin':
            admin_menu = ["📊 Admin Dashboard", "➕ Add Temple"]
        
        # Authentication menu items
        auth_menu = []
        if not st.session_state.authenticated:
            auth_menu = ["🔐 Login", "📝 Register"]
        else:
            auth_menu = ["👤 Profile"]
        
        # Combine all menu items
        all_menu_items = public_menu + admin_menu + auth_menu
        
        # Create navigation menu
        selected = option_menu(
            menu_title=None,
            options=all_menu_items,
            icons=None,
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#667eea"},
            }
        )
        
        # Map selection to page
        page_mapping = {
            "🏠 Home": "home",
            "🛕 All Temples": "temples",
            "📊 Admin Dashboard": "admin",
            "➕ Add Temple": "add_temple",
            "🔐 Login": "login",
            "📝 Register": "register",
            "👤 Profile": "profile"
        }
        
        st.session_state.page = page_mapping.get(selected, "home")

def show_login_page():
    """Display login page"""
    st.markdown("<div class='header'><h2 style='text-align: center;'>Login</h2></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                login_button = st.form_submit_button("Login", use_container_width=True)
            with col_btn2:
                if st.form_submit_button("Go to Register", use_container_width=True):
                    st.session_state.page = "register"
                    st.rerun()
            
            if login_button:
                if email and password:
                    success = login_user(email, password)
                    if success:
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                else:
                    st.warning("Please fill in all fields")

def show_register_page():
    """Display registration page"""
    st.markdown("<div class='header'><h2 style='text-align: center;'>Register</h2></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("register_form"):
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            role = st.selectbox("Role", ["user", "admin"])
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                register_button = st.form_submit_button("Register", use_container_width=True)
            with col_btn2:
                if st.form_submit_button("Go to Login", use_container_width=True):
                    st.session_state.page = "login"
                    st.rerun()
            
            if register_button:
                if name and email and password and confirm_password:
                    if password != confirm_password:
                        st.error("Passwords do not match!")
                    else:
                        success = register_user(name, email, password, role)
                        if success:
                            st.success("Registration successful! Please login.")
                            st.session_state.page = "login"
                            st.rerun()
                        else:
                            st.error("Email already exists or registration failed")
                else:
                    st.warning("Please fill in all fields")

def show_profile_page():
    """Display user profile page"""
    st.markdown("<div class='header'><h2>User Profile</h2></div>", unsafe_allow_html=True)
    
    if st.session_state.authenticated and st.session_state.user:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Profile Information")
            st.markdown(f"**Name:** {st.session_state.user['name']}")
            st.markdown(f"**Email:** {st.session_state.user['email']}")
            st.markdown(f"**Role:** {st.session_state.user['role'].title()}")
            st.markdown(f"**Member Since:** {st.session_state.user.get('created_at', 'N/A')}")
            
            if st.button("Logout", use_container_width=True):
                logout_user()
                st.rerun()
        
        with col2:
            st.markdown("### Account Settings")
            with st.expander("Change Password"):
                with st.form("change_password"):
                    new_password = st.text_input("New Password", type="password")
                    confirm_password = st.text_input("Confirm New Password", type="password")
                    
                    if st.form_submit_button("Update Password"):
                        if new_password != confirm_password:
                            st.error("New passwords do not match!")
                        else:
                            st.info("Password update functionality to be implemented")
            
            if st.session_state.user['role'] == 'admin':
                st.markdown("### Admin Actions")
                if st.button("Go to Admin Dashboard", use_container_width=True):
                    st.session_state.page = "admin"
                    st.rerun()

def main():
    """Main application entry point"""
    # Display header
    st.markdown("<div class='header'>", unsafe_allow_html=True)
    show_header()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display navigation
    show_navigation()
    
    # Route to appropriate page
    if st.session_state.page == "home":
        show_home_page()
    elif st.session_state.page == "temples":
        show_temple_list()
    elif st.session_state.page == "temple_detail":
        if st.session_state.selected_temple:
            show_temple_detail(st.session_state.selected_temple)
        else:
            st.session_state.page = "temples"
            st.rerun()
    elif st.session_state.page == "login":
        show_login_page()
    elif st.session_state.page == "register":
        show_register_page()
    elif st.session_state.page == "profile":
        if st.session_state.authenticated:
            show_profile_page()
        else:
            st.session_state.page = "login"
            st.rerun()
    elif st.session_state.page == "admin":
        if st.session_state.authenticated and st.session_state.user.get('role') == 'admin':
            show_admin_dashboard()
        else:
            st.error("Access denied. Admin privileges required.")
            st.session_state.page = "home"
    elif st.session_state.page == "add_temple":
        if st.session_state.authenticated and st.session_state.user.get('role') == 'admin':
            show_add_temple()
        else:
            st.error("Access denied. Admin privileges required.")
            st.session_state.page = "home"
    elif st.session_state.page == "edit_temple":
        if st.session_state.authenticated and st.session_state.user.get('role') == 'admin':
            if st.session_state.selected_temple:
                show_edit_temple(st.session_state.selected_temple)
            else:
                st.session_state.page = "admin"
                st.rerun()
        else:
            st.error("Access denied. Admin privileges required.")
            st.session_state.page = "home"

if __name__ == "__main__":
    main()
