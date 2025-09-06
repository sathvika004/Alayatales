"""
Alayatales - Temple Management System
A Streamlit application for managing temple information

Created with ❤️ for preserving and sharing temple heritage
Built using Streamlit, MongoDB, and Python

Author: Temple Heritage Team
Version: 1.0.0
License: MIT

Acknowledgments:
- Streamlit team for the amazing framework
- MongoDB for reliable data storage
- Pillow for image processing
- Plotly for beautiful visualizations
- All contributors and temple enthusiasts
"""

__version__ = "1.0.0"

import streamlit as st
import os
from dotenv import load_dotenv

# Try to import streamlit_option_menu, use fallback if not available
try:
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except ImportError:
    HAS_OPTION_MENU = False

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
        public_menu = ["🏠 Home", "🛕 All Temples", "ℹ️ About", "❓ Help"]
        
        # Admin menu items
        admin_menu = []
        if st.session_state.authenticated and st.session_state.user.get('role') == 'admin':
            admin_menu = ["📊 Admin Dashboard", "➕ Add Temple", "⚙️ Settings"]
        
        # Authentication menu items
        auth_menu = []
        if not st.session_state.authenticated:
            auth_menu = ["🔐 Login", "📝 Register"]
        else:
            auth_menu = ["👤 Profile"]
        
        # Combine all menu items
        all_menu_items = public_menu + admin_menu + auth_menu
        
        # Page mapping
        page_mapping = {
            "🏠 Home": "home",
            "🛕 All Temples": "temples",
            "ℹ️ About": "about",
            "❓ Help": "help",
            "📊 Admin Dashboard": "admin",
            "➕ Add Temple": "add_temple",
            "⚙️ Settings": "settings",
            "🔐 Login": "login",
            "📝 Register": "register",
            "👤 Profile": "profile"
        }
        
        # Use streamlit-option-menu if available, otherwise use buttons
        if HAS_OPTION_MENU:
            # Create navigation menu with option_menu
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
            st.session_state.page = page_mapping.get(selected, "home")
        else:
            # Fallback: Use regular Streamlit buttons
            for menu_item in all_menu_items:
                if st.button(menu_item, key=f"nav_{menu_item}", use_container_width=True):
                    st.session_state.page = page_mapping.get(menu_item, "home")
                    st.rerun()
            
            # Show current page indicator
            current_page = None
            for item, page in page_mapping.items():
                if page == st.session_state.page:
                    current_page = item
                    break
            if current_page:
                st.info(f"Current page: {current_page}")

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

def show_about_page():
    """Display about page with acknowledgments"""
    st.markdown("<div class='header'><h2 style='text-align: center;'>About Alayatales</h2></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### 🛕 Welcome to Alayatales
        
        **Alayatales** is a comprehensive temple management system designed to preserve and share the rich heritage of sacred temples. Our mission is to create a digital repository that celebrates the architectural beauty, spiritual significance, and cultural importance of temples worldwide.
        
        ### ✨ Features
        - 📸 **Image Gallery**: High-quality temple photographs with automatic compression
        - 🔍 **Smart Search**: Find temples by name, location, or description
        - ⏰ **Timing Information**: Complete visiting hours and schedule details
        - 👥 **User Management**: Secure authentication and role-based access
        - 📊 **Analytics**: Comprehensive statistics and insights
        - 📱 **Responsive Design**: Works seamlessly on all devices
        
        ### 🙏 Acknowledgments
        
        This project was made possible thanks to:
        
        **Technology Stack:**
        - 🚀 **Streamlit** - For the amazing web framework
        - 🍃 **MongoDB** - For reliable and scalable data storage
        - 🖼️ **Pillow (PIL)** - For advanced image processing
        - 📈 **Plotly** - For beautiful and interactive visualizations
        - 🐍 **Python** - For the powerful programming language
        
        **Special Thanks:**
        - 🌟 **Open Source Community** - For countless libraries and tools
        - 🏛️ **Temple Authorities** - For preserving our cultural heritage
        - 👨‍💻 **Developers** - Who contribute to making this platform better
        - 🙏 **Users** - Who help us document and share temple information
        
        ### 📄 License
        This project is open source and available under the **MIT License**.
        
        ### 🤝 Contributing
        We welcome contributions from the community! Whether it's:
        - 📝 Adding new temple information
        - 🐛 Reporting bugs or issues
        - 💡 Suggesting new features
        - 🔧 Contributing code improvements
        
        ### 📞 Contact
        For questions, suggestions, or collaboration opportunities, please reach out to our team.
        
        ---
        
        **Made with ❤️ for preserving temple heritage**
        
        *Version: 1.0.0*
        """)

def show_help_page():
    """Display help and documentation page"""
    st.markdown("<div class='header'><h2 style='text-align: center;'>Help & Documentation</h2></div>", unsafe_allow_html=True)
    
    # Create tabs for different help sections
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Getting Started", "🔍 Using the App", "👥 User Roles", "❓ FAQ"])
    
    with tab1:
        st.markdown("""
        ### 🚀 Getting Started with Alayatales
        
        Welcome to Alayatales! Here's how to get started:
        
        #### 1. **Registration**
        - Click on "📝 Register" in the sidebar
        - Fill in your details (Name, Email, Password)
        - Choose your role (User or Admin)
        - Click "Register" to create your account
        
        #### 2. **Login**
        - Click on "🔐 Login" in the sidebar
        - Enter your email and password
        - Click "Login" to access your account
        
        #### 3. **Explore Temples**
        - Visit "🛕 All Temples" to browse all temples
        - Use the search bar to find specific temples
        - Click "View Details" on any temple card to see more information
        
        #### 4. **Admin Features** (Admin users only)
        - Access "📊 Admin Dashboard" for statistics
        - Use "➕ Add Temple" to add new temples
        - Manage users and temple information
        """)
    
    with tab2:
        st.markdown("""
        ### 🔍 Using the Application
        
        #### **Navigation**
        - Use the sidebar menu to navigate between pages
        - The current page is highlighted in the navigation
        
        #### **Searching Temples**
        - Use the search bar on the home page or temples page
        - Search by temple name, location, or description
        - Results are displayed instantly as you type
        
        #### **Viewing Temple Details**
        - Click "View Details" on any temple card
        - Browse through the image gallery
        - Check visiting timings and other information
        - Use navigation buttons to go back
        
        #### **Image Upload** (Admin only)
        - Maximum 5 images per temple
        - Each image can be up to 5MB
        - Supported formats: PNG, JPG, JPEG
        - Images are automatically compressed for optimal storage
        
        #### **Profile Management**
        - Access your profile from "👤 Profile" in the sidebar
        - Update your password in the Account Settings section
        - View your account information and role
        """)
    
    with tab3:
        st.markdown("""
        ### 👥 User Roles & Permissions
        
        #### **👤 Regular User**
        **Can do:**
        - ✅ Browse all temples
        - ✅ Search for temples
        - ✅ View temple details and images
        - ✅ Access their profile
        - ✅ Change their password
        
        **Cannot do:**
        - ❌ Add new temples
        - ❌ Edit temple information
        - ❌ Delete temples
        - ❌ Access admin dashboard
        - ❌ Manage other users
        
        #### **👨‍💼 Admin User**
        **Can do everything a regular user can, plus:**
        - ✅ Add new temples with images
        - ✅ Edit existing temple information
        - ✅ Delete temples
        - ✅ Access admin dashboard with statistics
        - ✅ View user management information
        - ✅ Access application settings
        
        #### **🔒 Security Features**
        - Secure password hashing
        - Session-based authentication
        - Role-based access control
        - Automatic logout on session expiry
        """)
    
    with tab4:
        st.markdown("""
        ### ❓ Frequently Asked Questions
        
        #### **General Questions**
        
        **Q: Is Alayatales free to use?**
        A: Yes! Alayatales is completely free and open source.
        
        **Q: Can I use this without creating an account?**
        A: You can browse temples without an account, but you need to register to access additional features.
        
        **Q: How do I become an admin?**
        A: Admin access is typically granted by existing administrators. Contact the system administrator for admin privileges.
        
        #### **Technical Questions**
        
        **Q: What image formats are supported?**
        A: We support PNG, JPG, and JPEG formats. Images are automatically compressed for optimal storage.
        
        **Q: Why are my images being compressed?**
        A: Images are compressed to ensure fast loading times and efficient storage while maintaining good quality.
        
        **Q: What's the maximum file size for images?**
        A: Each image can be up to 5MB, and you can upload up to 5 images per temple.
        
        **Q: Can I edit temple information after adding it?**
        A: Yes, admin users can edit temple information anytime from the temple detail page.
        
        #### **Troubleshooting**
        
        **Q: I forgot my password. How do I reset it?**
        A: Currently, password reset needs to be done by an administrator. Contact support for assistance.
        
        **Q: The app is loading slowly. What can I do?**
        A: This might be due to large images or network connectivity. Try refreshing the page or check your internet connection.
        
        **Q: I'm getting an error when uploading images. What's wrong?**
        A: Check that your images are under 5MB and in supported formats (PNG, JPG, JPEG). Also ensure you're not exceeding the 5-image limit per temple.
        
        ---
        
        **Still need help?** Contact our support team for assistance.
        """)

def show_settings_page():
    """Display settings page for admin users"""
    st.markdown("<div class='header'><h2>⚙️ Application Settings</h2></div>", unsafe_allow_html=True)
    
    if not st.session_state.authenticated or st.session_state.user.get('role') != 'admin':
        st.error("Access denied. Admin privileges required.")
        return
    
    # Application Information
    st.markdown("### 📊 Application Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("App Version", "1.0.0")
    with col2:
        st.metric("Database Status", "Connected" if init_database() else "Disconnected")
    with col3:
        from models import get_temple_stats
        stats = get_temple_stats()
        st.metric("Total Records", stats['total_temples'] + stats['total_users'])
    
    st.markdown("---")
    
    # Database Management
    st.markdown("### 🗄️ Database Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Export Data")
        if st.button("📤 Export All Temples", use_container_width=True):
            try:
                from models import get_all_temples
                import json
                temples = get_all_temples()
                # Remove images for export to reduce size
                export_data = []
                for temple in temples:
                    temple_copy = temple.copy()
                    temple_copy.pop('images', None)  # Remove images
                    export_data.append(temple_copy)
                
                json_data = json.dumps(export_data, indent=2, default=str)
                st.download_button(
                    label="💾 Download Temple Data (JSON)",
                    data=json_data,
                    file_name="temples_export.json",
                    mime="application/json"
                )
                st.success(f"✅ Ready to export {len(temples)} temples")
            except Exception as e:
                st.error(f"Export failed: {str(e)}")
    
    with col2:
        st.markdown("#### System Maintenance")
        if st.button("🧹 Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Cache cleared successfully!")
        
        if st.button("🔄 Refresh Statistics", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Statistics refreshed!")
    
    st.markdown("---")
    
    # User Management
    st.markdown("### 👥 User Management")
    
    from models import get_all_users
    users = get_all_users()
    
    if users:
        st.markdown(f"**Total Users:** {len(users)}")
        
        # User statistics
        admin_count = sum(1 for user in users if user.get('role') == 'admin')
        user_count = len(users) - admin_count
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Admin Users", admin_count)
        with col2:
            st.metric("Regular Users", user_count)
        
        # User table with actions
        st.markdown("#### User List")
        for user in users:
            with st.expander(f"👤 {user.get('name', 'Unknown')} ({user.get('email', 'No email')})"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Role:** {user.get('role', 'user').title()}")
                    st.write(f"**Created:** {str(user.get('created_at', 'Unknown'))[:10]}")
                    st.write(f"**ID:** {user.get('_id', 'Unknown')}")
                
                with col2:
                    if user.get('_id') != st.session_state.user['id']:  # Can't delete self
                        if st.button(f"🗑️ Delete", key=f"delete_user_{user['_id']}"):
                            if st.session_state.get(f'confirm_delete_user_{user["_id"]}', False):
                                from models import delete_user
                                if delete_user(user['_id']):
                                    st.success("User deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete user")
                            else:
                                st.session_state[f'confirm_delete_user_{user["_id"]}'] = True
                                st.warning("Click again to confirm deletion")
                
                with col3:
                    if user.get('role') == 'user':
                        if st.button(f"⬆️ Make Admin", key=f"promote_{user['_id']}"):
                            from models import update_user
                            if update_user(user['_id'], {'role': 'admin'}):
                                st.success("User promoted to admin!")
                                st.rerun()
                    elif user.get('_id') != st.session_state.user['id']:  # Can't demote self
                        if st.button(f"⬇️ Make User", key=f"demote_{user['_id']}"):
                            from models import update_user
                            if update_user(user['_id'], {'role': 'user'}):
                                st.success("Admin demoted to user!")
                                st.rerun()
    
    st.markdown("---")
    
    # Application Configuration
    st.markdown("### ⚙️ Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Upload Settings")
        st.info("📁 Max file size: 5MB per image")
        st.info("🖼️ Max images per temple: 5")
        st.info("📐 Max image dimension: 800px")
        st.info("🎨 Compression quality: 85%")
    
    with col2:
        st.markdown("#### Database Settings")
        st.info("🗄️ Database: MongoDB")
        st.info("📊 Document size limit: 15MB")
        st.info("🔒 Authentication: Session-based")
        st.info("🔐 Password hashing: SHA-256")

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
                    old_password = st.text_input("Current Password", type="password")
                    new_password = st.text_input("New Password", type="password")
                    confirm_password = st.text_input("Confirm New Password", type="password")
                    
                    if st.form_submit_button("Update Password"):
                        if not old_password or not new_password or not confirm_password:
                            st.error("Please fill in all password fields!")
                        elif new_password != confirm_password:
                            st.error("New passwords do not match!")
                        elif len(new_password) < 6:
                            st.error("New password must be at least 6 characters long!")
                        else:
                            from auth import update_user_password
                            success = update_user_password(st.session_state.user['id'], old_password, new_password)
                            if success:
                                st.success("Password updated successfully!")
                            else:
                                st.error("Failed to update password. Please check your current password.")
            
            if st.session_state.user['role'] == 'admin':
                st.markdown("### Admin Actions")
                if st.button("Go to Admin Dashboard", use_container_width=True):
                    st.session_state.page = "admin"
                    st.rerun()

def show_footer():
    """Display footer with acknowledgments"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem; margin-top: 2rem;'>
        <p><strong>Alayatales v1.0.0</strong> - Made with ❤️ for preserving temple heritage</p>
        <p>Built with 🚀 Streamlit • 🍃 MongoDB • 🐍 Python • 🖼️ Pillow • 📈 Plotly</p>
        <p>© 2024 Temple Heritage Team • Open Source under MIT License</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    try:
        # Display header
        st.markdown("<div class='header'>", unsafe_allow_html=True)
        show_header()
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display navigation
        show_navigation()
    except Exception as e:
        st.error("An error occurred while loading the application.")
        st.error(f"Error details: {str(e)}")
        st.info("Please refresh the page or contact support if the problem persists.")
    
    # Route to appropriate page
    try:
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
        elif st.session_state.page == "about":
            show_about_page()
        elif st.session_state.page == "help":
            show_help_page()
        elif st.session_state.page == "settings":
            if st.session_state.authenticated and st.session_state.user.get('role') == 'admin':
                show_settings_page()
            else:
                st.error("Access denied. Admin privileges required.")
                st.session_state.page = "home"
    except Exception as e:
        st.error(f"An error occurred while loading the page: {str(e)}")
        st.info("Please try refreshing the page or go back to home.")
        if st.button("🏠 Go to Home"):
            st.session_state.page = "home"
            st.rerun()
    
    # Display footer on all pages
    show_footer()

if __name__ == "__main__":
    main()
