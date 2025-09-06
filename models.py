"""
Database models and MongoDB connection
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from bson.errors import InvalidId
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_config(key: str, default: str = None) -> str:
    """Get configuration from environment or Streamlit secrets"""
    # Try Streamlit secrets first (for deployment)
    try:
        return st.secrets.get(key, os.getenv(key, default))
    except:
        # Fall back to environment variables (for local development)
        return os.getenv(key, default)

# MongoDB connection
@st.cache_resource
def get_database_connection():
    """Create and return MongoDB connection"""
    mongodb_uri = get_config('MONGODB_URI', 'mongodb://localhost:27017/')
    try:
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        return client
    except Exception as e:
        st.error(f"❌ MongoDB Connection Error: {e}")
        if "mongodb+srv" in mongodb_uri:
            st.error("Failed to connect to MongoDB Atlas. Please check:")
            st.info("1. Your internet connection")
            st.info("2. MongoDB Atlas credentials in secrets/environment")
            st.info("3. IP whitelist settings in MongoDB Atlas")
        else:
            st.error("Please ensure MongoDB is installed and running.")
            st.info("For local development: Install MongoDB")
            st.info("For Streamlit Cloud: Use MongoDB Atlas")
        return None

def init_database():
    """Initialize database and create indexes"""
    client = get_database_connection()
    if client is None:
        return None
    
    try:
        db = client[get_config('DB_NAME', 'alayatales')]
        
        # Create indexes
        db.users.create_index("email", unique=True)
        db.temples.create_index("name")
        
        return db
    except Exception as e:
        st.error(f"Database initialization error: {e}")
        return None

def get_db():
    """Get database instance"""
    client = get_database_connection()
    if client is None:
        return None
    return client[get_config('DB_NAME', 'alayatales')]

def is_valid_object_id(oid: str) -> bool:
    """Check if string is a valid ObjectId"""
    try:
        ObjectId(oid)
        return True
    except (InvalidId, TypeError):
        return False

def validate_document_size(document: Dict) -> bool:
    """Validate that document size is within MongoDB limits"""
    import json
    import sys
    
    # Calculate approximate document size
    doc_json = json.dumps(document, default=str)
    doc_size = sys.getsizeof(doc_json)
    
    # MongoDB document limit is 16MB (16,777,216 bytes)
    # We'll use 15MB as safe limit to account for metadata
    max_size = 15 * 1024 * 1024  # 15MB
    
    if doc_size > max_size:
        st.error(f"❌ Document too large: {doc_size//1024//1024}MB (max: 15MB)")
        st.error("Please reduce image sizes or number of images.")
        return False
    
    return True

# Temple Model Functions
def create_temple(temple_data: Dict) -> Optional[str]:
    """Create a new temple"""
    try:
        db = get_db()
        if db is None:
            return None
            
        temple_data['created_at'] = datetime.utcnow()
        temple_data['updated_at'] = datetime.utcnow()
        
        # Ensure timings is properly formatted
        if 'timings' not in temple_data:
            temple_data['timings'] = []
        
        # Ensure images is a list
        if 'images' not in temple_data:
            temple_data['images'] = []
        elif not isinstance(temple_data['images'], list):
            temple_data['images'] = [temple_data['images']]
        
        # Validate document size before inserting
        if not validate_document_size(temple_data):
            return None
        
        result = db.temples.insert_one(temple_data)
        return str(result.inserted_id)
    except Exception as e:
        st.error(f"Error creating temple: {e}")
        return None

def get_all_temples() -> List[Dict]:
    """Get all temples"""
    try:
        db = get_db()
        temples = list(db.temples.find())
        # Convert ObjectId to string
        for temple in temples:
            temple['_id'] = str(temple['_id'])
        return temples
    except Exception as e:
        st.error(f"Error fetching temples: {e}")
        return []

def get_temple_by_id(temple_id: str) -> Optional[Dict]:
    """Get temple by ID"""
    try:
        # Validate ObjectId format first
        if not is_valid_object_id(temple_id):
            if st.session_state.get('debug_mode', False):
                st.error(f"Debug: Invalid ObjectId format: {temple_id}")
            return None
            
        db = get_db()
        if db is None:
            st.error("Database connection failed")
            return None
            
        # Debug information
        if st.session_state.get('debug_mode', False):
            st.info(f"Debug: Searching for temple with ID: {temple_id}")
            
        temple = db.temples.find_one({"_id": ObjectId(temple_id)})
        if temple:
            temple['_id'] = str(temple['_id'])
            if st.session_state.get('debug_mode', False):
                st.success(f"Debug: Temple found: {temple.get('name', 'Unknown')}")
        else:
            if st.session_state.get('debug_mode', False):
                st.warning(f"Debug: No temple found with ID: {temple_id}")
        return temple
    except Exception as e:
        st.error(f"Error fetching temple: {e}")
        if st.session_state.get('debug_mode', False):
            st.error(f"Debug: Exception details: {str(e)}")
        return None

def update_temple(temple_id: str, update_data: Dict) -> bool:
    """Update temple"""
    try:
        db = get_db()
        if db is None:
            return False
            
        update_data['updated_at'] = datetime.utcnow()
        
        # Remove _id if present in update data
        update_data.pop('_id', None)
        
        # Get current temple data to validate final document size
        current_temple = db.temples.find_one({"_id": ObjectId(temple_id)})
        if current_temple:
            # Merge current data with updates for size validation
            merged_data = {**current_temple, **update_data}
            if not validate_document_size(merged_data):
                return False
        
        result = db.temples.update_one(
            {"_id": ObjectId(temple_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except Exception as e:
        st.error(f"Error updating temple: {e}")
        return False

def delete_temple(temple_id: str) -> bool:
    """Delete temple"""
    try:
        db = get_db()
        result = db.temples.delete_one({"_id": ObjectId(temple_id)})
        return result.deleted_count > 0
    except Exception as e:
        st.error(f"Error deleting temple: {e}")
        return False

def search_temples(query: str) -> List[Dict]:
    """Search temples by name or location"""
    try:
        db = get_db()
        temples = list(db.temples.find({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"location": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        }))
        for temple in temples:
            temple['_id'] = str(temple['_id'])
        return temples
    except Exception as e:
        st.error(f"Error searching temples: {e}")
        return []

# User Model Functions
def create_user(user_data: Dict) -> Optional[str]:
    """Create a new user"""
    try:
        db = get_db()
        user_data['created_at'] = datetime.utcnow()
        user_data['updated_at'] = datetime.utcnow()
        
        # Set default role if not provided
        if 'role' not in user_data:
            user_data['role'] = 'user'
        
        result = db.users.insert_one(user_data)
        return str(result.inserted_id)
    except DuplicateKeyError:
        return None
    except Exception as e:
        st.error(f"Error creating user: {e}")
        return None

def get_user_by_email(email: str) -> Optional[Dict]:
    """Get user by email"""
    try:
        db = get_db()
        user = db.users.find_one({"email": email})
        if user:
            user['_id'] = str(user['_id'])
        return user
    except Exception as e:
        st.error(f"Error fetching user: {e}")
        return None

def get_user_by_id(user_id: str) -> Optional[Dict]:
    """Get user by ID"""
    try:
        db = get_db()
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
        return user
    except Exception as e:
        st.error(f"Error fetching user: {e}")
        return None

def update_user(user_id: str, update_data: Dict) -> bool:
    """Update user"""
    try:
        db = get_db()
        update_data['updated_at'] = datetime.utcnow()
        
        # Remove _id if present
        update_data.pop('_id', None)
        
        result = db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except Exception as e:
        st.error(f"Error updating user: {e}")
        return False

def get_all_users() -> List[Dict]:
    """Get all users (admin function)"""
    try:
        db = get_db()
        users = list(db.users.find())
        for user in users:
            user['_id'] = str(user['_id'])
            # Don't send password to frontend
            user.pop('password', None)
        return users
    except Exception as e:
        st.error(f"Error fetching users: {e}")
        return []

def delete_user(user_id: str) -> bool:
    """Delete user"""
    try:
        db = get_db()
        result = db.users.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    except Exception as e:
        st.error(f"Error deleting user: {e}")
        return False

# Temple Timing Helper Functions
def format_timing(timing: Dict) -> str:
    """Format timing dictionary to readable string"""
    morning = f"{timing.get('morningOpening', 'N/A')} - {timing.get('morningClosing', 'N/A')}"
    evening = f"{timing.get('eveningOpening', 'N/A')} - {timing.get('eveningClosing', 'N/A')}"
    return f"Morning: {morning}, Evening: {evening}"

def parse_timing_string(timing_str: str) -> Dict:
    """Parse timing string to dictionary"""
    # Example: "6:00 AM - 12:00 PM, 4:00 PM - 8:00 PM"
    try:
        parts = timing_str.split(',')
        morning_parts = parts[0].strip().split(' - ')
        evening_parts = parts[1].strip().split(' - ') if len(parts) > 1 else ['', '']
        
        return {
            'morningOpening': morning_parts[0].strip(),
            'morningClosing': morning_parts[1].strip() if len(morning_parts) > 1 else '',
            'eveningOpening': evening_parts[0].strip(),
            'eveningClosing': evening_parts[1].strip() if len(evening_parts) > 1 else ''
        }
    except:
        return {
            'morningOpening': '',
            'morningClosing': '',
            'eveningOpening': '',
            'eveningClosing': ''
        }

# Statistics Functions (for admin dashboard)
def get_temple_stats() -> Dict:
    """Get temple statistics"""
    try:
        db = get_db()
        if db is None:
            return {
                "total_temples": 0,
                "total_users": 0,
                "admin_users": 0,
                "temples_by_location": []
            }
            
        total_temples = db.temples.count_documents({})
        total_users = db.users.count_documents({})
        admin_users = db.users.count_documents({"role": "admin"})
        
        # Get temples by location
        temples_by_location = list(db.temples.aggregate([
            {"$group": {"_id": "$location", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]))
        
        return {
            "total_temples": total_temples,
            "total_users": total_users,
            "admin_users": admin_users,
            "temples_by_location": temples_by_location
        }
    except Exception as e:
        st.error(f"Error fetching statistics: {e}")
        return {
            "total_temples": 0,
            "total_users": 0,
            "admin_users": 0,
            "temples_by_location": []
        }

def create_sample_temples() -> bool:
    """Create sample temples for testing"""
    try:
        db = get_db()
        if db is None:
            return False
            
        # Check if temples already exist
        if db.temples.count_documents({}) > 0:
            return True
            
        sample_temples = [
            {
                "name": "Golden Temple",
                "location": "Amritsar, Punjab",
                "description": "The Golden Temple, also known as Harmandir Sahib, is a gurdwara located in the city of Amritsar, Punjab, India. It is the holiest gurdwara and the most important pilgrimage site of Sikhism.",
                "images": ["https://via.placeholder.com/400x300?text=Golden+Temple"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Meenakshi Temple",
                "location": "Madurai, Tamil Nadu",
                "description": "Meenakshi Temple is a historic Hindu temple located on the southern bank of the Vaigai River in the temple city of Madurai, Tamil Nadu, India.",
                "images": ["https://via.placeholder.com/400x300?text=Meenakshi+Temple"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Lotus Temple",
                "location": "New Delhi",
                "description": "The Lotus Temple, located in Delhi, India, is a Baháʼí House of Worship that was dedicated in December 1986. Notable for its flowerlike shape, it has become a prominent attraction in the city.",
                "images": ["https://via.placeholder.com/400x300?text=Lotus+Temple"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        result = db.temples.insert_many(sample_temples)
        return len(result.inserted_ids) > 0
        
    except Exception as e:
        st.error(f"Error creating sample temples: {e}")
        return False
