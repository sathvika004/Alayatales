"""
Utility functions for Alayatales Temple Management System
"""

import os
import re
import json
import base64
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import streamlit as st
from PIL import Image
import io

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> Dict[str, Any]:
    """
    Validate password strength
    Returns dict with 'valid' boolean and 'message' string
    """
    if len(password) < 8:
        return {'valid': False, 'message': 'Password must be at least 8 characters long'}
    
    if not re.search(r'[A-Z]', password):
        return {'valid': False, 'message': 'Password must contain at least one uppercase letter'}
    
    if not re.search(r'[a-z]', password):
        return {'valid': False, 'message': 'Password must contain at least one lowercase letter'}
    
    if not re.search(r'\d', password):
        return {'valid': False, 'message': 'Password must contain at least one number'}
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return {'valid': False, 'message': 'Password must contain at least one special character'}
    
    return {'valid': True, 'message': 'Password is strong'}

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    return filename

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def compress_image(image_data: bytes, quality: int = 85, max_dimension: int = 800) -> bytes:
    """
    Compress and resize image
    Returns compressed image as bytes
    """
    try:
        # Open image
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        # Resize if too large
        if image.width > max_dimension or image.height > max_dimension:
            image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
        
        # Compress
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        return output.getvalue()
    
    except Exception as e:
        st.error(f"Error compressing image: {str(e)}")
        return image_data

def generate_thumbnail(image_data: bytes, size: tuple = (150, 150)) -> str:
    """Generate thumbnail and return as base64 string"""
    try:
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=70)
        thumbnail_data = output.getvalue()
        
        return base64.b64encode(thumbnail_data).decode()
    except Exception:
        return ""

def calculate_reading_time(text: str) -> int:
    """Calculate estimated reading time in minutes"""
    words = len(text.split())
    # Average reading speed: 200 words per minute
    minutes = max(1, round(words / 200))
    return minutes

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def format_datetime(dt: datetime, format_type: str = "default") -> str:
    """Format datetime for display"""
    if not dt:
        return "Unknown"
    
    formats = {
        "default": "%Y-%m-%d %H:%M",
        "date_only": "%Y-%m-%d",
        "time_only": "%H:%M",
        "full": "%A, %B %d, %Y at %I:%M %p",
        "relative": None  # Special case for relative time
    }
    
    if format_type == "relative":
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    return dt.strftime(formats.get(format_type, formats["default"]))

def generate_slug(text: str) -> str:
    """Generate URL-friendly slug from text"""
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def validate_image_file(file) -> Dict[str, Any]:
    """Validate uploaded image file"""
    if not file:
        return {'valid': False, 'message': 'No file provided'}
    
    # Check file size (5MB limit)
    if file.size > 5 * 1024 * 1024:
        return {'valid': False, 'message': 'File size exceeds 5MB limit'}
    
    # Check file type
    allowed_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
    if file.type not in allowed_types:
        return {'valid': False, 'message': 'Invalid file type. Only PNG, JPEG, GIF, and WebP are allowed'}
    
    # Try to open as image
    try:
        image = Image.open(file)
        image.verify()
        return {'valid': True, 'message': 'Valid image file'}
    except Exception:
        return {'valid': False, 'message': 'Invalid or corrupted image file'}

def create_backup_filename(original_name: str) -> str:
    """Create backup filename with timestamp"""
    name, ext = os.path.splitext(original_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_backup_{timestamp}{ext}"

def log_activity(user_id: str, action: str, details: str = "") -> None:
    """Log user activity (placeholder for future implementation)"""
    # This could be expanded to log to a file or database
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'user_id': user_id,
        'action': action,
        'details': details
    }
    # For now, just store in session state
    if 'activity_log' not in st.session_state:
        st.session_state.activity_log = []
    st.session_state.activity_log.append(log_entry)

def get_user_activity_log(user_id: str, limit: int = 10) -> List[Dict]:
    """Get recent user activity"""
    if 'activity_log' not in st.session_state:
        return []
    
    user_activities = [
        log for log in st.session_state.activity_log 
        if log.get('user_id') == user_id
    ]
    
    # Sort by timestamp (most recent first)
    user_activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return user_activities[:limit]

def clean_html_tags(text: str) -> str:
    """Remove HTML tags from text"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def generate_color_from_string(text: str) -> str:
    """Generate a consistent color from string (for avatars, etc.)"""
    hash_object = hashlib.md5(text.encode())
    hex_dig = hash_object.hexdigest()
    
    # Take first 6 characters as color
    color = "#" + hex_dig[:6]
    return color

def create_breadcrumb(pages: List[str]) -> str:
    """Create breadcrumb navigation HTML"""
    if not pages:
        return ""
    
    breadcrumb_items = []
    for i, page in enumerate(pages):
        if i == len(pages) - 1:  # Last item (current page)
            breadcrumb_items.append(f'<span class="breadcrumb-current">{page}</span>')
        else:
            breadcrumb_items.append(f'<span class="breadcrumb-item">{page}</span>')
    
    return ' > '.join(breadcrumb_items)

def get_system_info() -> Dict[str, Any]:
    """Get system information for debugging"""
    import platform
    import sys
    
    return {
        'python_version': sys.version,
        'platform': platform.platform(),
        'processor': platform.processor(),
        'architecture': platform.architecture(),
        'streamlit_version': st.__version__ if hasattr(st, '__version__') else 'Unknown'
    }

def export_to_json(data: Any, filename: str = None) -> str:
    """Export data to JSON string"""
    try:
        return json.dumps(data, indent=2, default=str, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error exporting to JSON: {str(e)}")
        return "{}"

def import_from_json(json_string: str) -> Any:
    """Import data from JSON string"""
    try:
        return json.loads(json_string)
    except Exception as e:
        st.error(f"Error importing from JSON: {str(e)}")
        return None

def create_download_link(data: str, filename: str, mime_type: str = "text/plain") -> str:
    """Create download link for data"""
    b64_data = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:{mime_type};base64,{b64_data}" download="{filename}">Download {filename}</a>'
    return href

def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename)[1].lower()

def is_valid_url(url: str) -> bool:
    """Check if URL is valid"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def create_progress_bar(current: int, total: int, width: int = 20) -> str:
    """Create ASCII progress bar"""
    if total == 0:
        return "[" + "=" * width + "]"
    
    progress = current / total
    filled = int(width * progress)
    bar = "=" * filled + "-" * (width - filled)
    percentage = int(progress * 100)
    
    return f"[{bar}] {percentage}%"

def get_mime_type(filename: str) -> str:
    """Get MIME type from filename"""
    ext = get_file_extension(filename)
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.pdf': 'application/pdf',
        '.json': 'application/json',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript'
    }
    return mime_types.get(ext, 'application/octet-stream')

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount"""
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'INR': '₹',
        'JPY': '¥'
    }
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"

def generate_qr_code_url(text: str, size: str = "150x150") -> str:
    """Generate QR code URL using Google Charts API"""
    import urllib.parse
    encoded_text = urllib.parse.quote(text)
    return f"https://chart.googleapis.com/chart?chs={size}&cht=qr&chl={encoded_text}"

# Cache frequently used functions
@st.cache_data
def cached_format_datetime(dt_str: str, format_type: str = "default") -> str:
    """Cached version of format_datetime"""
    try:
        dt = datetime.fromisoformat(dt_str)
        return format_datetime(dt, format_type)
    except:
        return "Invalid date"

@st.cache_data
def cached_truncate_text(text: str, max_length: int = 100) -> str:
    """Cached version of truncate_text"""
    return truncate_text(text, max_length)

# Constants
DEFAULT_IMAGE_QUALITY = 85
DEFAULT_MAX_DIMENSION = 800
DEFAULT_THUMBNAIL_SIZE = (150, 150)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_TYPES = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']