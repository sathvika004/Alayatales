"""
Temple management pages for the Streamlit application
"""

import streamlit as st
from typing import Dict, List, Optional
import base64
from PIL import Image
import io
from datetime import datetime
from models import (
    get_all_temples,
    get_temple_by_id,
    create_temple,
    update_temple,
    delete_temple,
    search_temples,
    format_timing,
    get_temple_stats,
    get_all_users
)
from auth import is_admin, require_auth

def show_home_page():
    """Display the home page with featured temples"""
    st.markdown("<h1 style='text-align: center;'>Welcome to Alayatales 🛕</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Discover and explore sacred temples</p>", unsafe_allow_html=True)
    
    # Search bar
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        search_query = st.text_input("🔍 Search temples by name or location", placeholder="Enter temple name or location...")
        
    # Get temples
    if search_query:
        temples = search_temples(search_query)
        st.markdown(f"### Search Results for '{search_query}'")
    else:
        temples = get_all_temples()[:6]  # Show only 6 featured temples on home
        st.markdown("### Featured Temples")
    
    if temples:
        # Display temples in a grid
        cols = st.columns(3)
        for idx, temple in enumerate(temples):
            with cols[idx % 3]:
                display_temple_card(temple)
    else:
        st.info("No temples found. Please check back later!")
    
    # Call to action
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("View All Temples", use_container_width=True):
            st.session_state.page = "temples"
            st.rerun()

def show_temple_list():
    """Display all temples in a list/grid format"""
    st.markdown("## 🛕 All Temples")
    
    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        search_query = st.text_input("Search", placeholder="Search by name or location...")
    with col2:
        # Get unique locations for filter
        all_temples = get_all_temples()
        locations = list(set([t.get('location', '') for t in all_temples if t.get('location')]))
        locations.insert(0, "All Locations")
        selected_location = st.selectbox("Filter by Location", locations)
    with col3:
        sort_by = st.selectbox("Sort by", ["Name", "Location", "Recently Added"])
    
    # Get filtered temples
    if search_query:
        temples = search_temples(search_query)
    elif selected_location and selected_location != "All Locations":
        temples = [t for t in all_temples if t.get('location') == selected_location]
    else:
        temples = all_temples
    
    # Sort temples
    if sort_by == "Name":
        temples.sort(key=lambda x: x.get('name', ''))
    elif sort_by == "Location":
        temples.sort(key=lambda x: x.get('location', ''))
    elif sort_by == "Recently Added":
        temples.sort(key=lambda x: x.get('created_at', datetime.min), reverse=True)
    
    # Display temples
    if temples:
        st.markdown(f"**Found {len(temples)} temples**")
        
        # Display in grid
        cols = st.columns(3)
        for idx, temple in enumerate(temples):
            with cols[idx % 3]:
                display_temple_card(temple)
    else:
        st.info("No temples found matching your criteria.")

def display_temple_card(temple: Dict):
    """Display a single temple card"""
    with st.container():
        # Create a card-like container
        st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
        """, unsafe_allow_html=True)
        
        # Display image if available
        if temple.get('images') and len(temple['images']) > 0:
            # If image is base64 encoded
            if temple['images'][0].startswith('data:image'):
                st.markdown(f"""
                <img src="{temple['images'][0]}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 5px;">
                """, unsafe_allow_html=True)
            else:
                # If image is a URL or file path
                try:
                    st.image(temple['images'][0], use_container_width=True)
                except:
                    st.image("https://via.placeholder.com/300x200?text=Temple+Image", use_container_width=True)
        else:
            st.image("https://via.placeholder.com/300x200?text=No+Image", use_container_width=True)
        
        # Temple info
        st.markdown(f"### {temple.get('name', 'Unknown Temple')}")
        st.markdown(f"📍 **Location:** {temple.get('location', 'Unknown')}")
        
        # Description (truncated)
        description = temple.get('description', 'No description available.')
        if len(description) > 100:
            description = description[:100] + "..."
        st.markdown(description)
        
        # View details button
        if st.button(f"View Details", key=f"view_{temple['_id']}"):
            st.session_state.selected_temple = temple['_id']
            st.session_state.page = "temple_detail"
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_temple_detail(temple_id: str):
    """Display detailed view of a single temple"""
    temple = get_temple_by_id(temple_id)
    
    if not temple:
        st.error("Temple not found!")
        if st.button("Back to Temples"):
            st.session_state.page = "temples"
            st.rerun()
        return
    
    # Back button
    if st.button("← Back to Temples"):
        st.session_state.page = "temples"
        st.rerun()
    
    # Temple name and location
    st.markdown(f"# {temple.get('name', 'Unknown Temple')}")
    st.markdown(f"### 📍 {temple.get('location', 'Unknown Location')}")
    
    # Image gallery
    if temple.get('images') and len(temple['images']) > 0:
        st.markdown("### 📸 Image Gallery")
        
        # Main image
        selected_image = st.select_slider(
            "Select image",
            options=range(len(temple['images'])),
            format_func=lambda x: f"Image {x + 1}"
        )
        
        # Display selected image
        if temple['images'][selected_image].startswith('data:image'):
            st.markdown(f"""
            <img src="{temple['images'][selected_image]}" style="width: 100%; max-height: 500px; object-fit: contain; border-radius: 10px;">
            """, unsafe_allow_html=True)
        else:
            try:
                st.image(temple['images'][selected_image], use_container_width=True)
            except:
                st.image("https://via.placeholder.com/600x400?text=Image+Not+Available", use_container_width=True)
        
        # Thumbnail gallery
        if len(temple['images']) > 1:
            cols = st.columns(min(len(temple['images']), 5))
            for idx, img in enumerate(temple['images'][:5]):
                with cols[idx]:
                    if st.button(f"", key=f"thumb_{idx}", help=f"Image {idx + 1}"):
                        pass  # Image selection is handled by select_slider
    
    # Temple information
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Description")
        st.write(temple.get('description', 'No description available.'))
    
    with col2:
        st.markdown("### ⏰ Timings")
        timings = temple.get('timings', [])
        if timings:
            for idx, timing in enumerate(timings):
                st.markdown(f"**Schedule {idx + 1}:**")
                st.markdown(f"🌅 Morning: {timing.get('morningOpening', 'N/A')} - {timing.get('morningClosing', 'N/A')}")
                st.markdown(f"🌆 Evening: {timing.get('eveningOpening', 'N/A')} - {timing.get('eveningClosing', 'N/A')}")
                st.markdown("---")
        else:
            st.info("Timing information not available")
    
    # Admin actions
    if is_admin():
        st.markdown("---")
        st.markdown("### Admin Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Edit Temple", use_container_width=True):
                st.session_state.selected_temple = temple_id
                st.session_state.page = "edit_temple"
                st.rerun()
        with col2:
            if st.button("🗑️ Delete Temple", use_container_width=True, type="secondary"):
                if st.checkbox("Confirm deletion"):
                    if delete_temple(temple_id):
                        st.success("Temple deleted successfully!")
                        st.session_state.page = "temples"
                        st.rerun()
                    else:
                        st.error("Failed to delete temple")

def show_add_temple():
    """Display form to add a new temple"""
    st.markdown("## ➕ Add New Temple")
    
    if not is_admin():
        st.error("Access denied. Admin privileges required.")
        return
    
    with st.form("add_temple_form"):
        # Basic information
        st.markdown("### Basic Information")
        name = st.text_input("Temple Name *", placeholder="Enter temple name")
        location = st.text_input("Location *", placeholder="Enter location")
        description = st.text_area("Description *", placeholder="Enter temple description", height=150)
        
        # Timings
        st.markdown("### Timings")
        num_timings = st.number_input("Number of timing schedules", min_value=1, max_value=5, value=1)
        
        timings = []
        for i in range(int(num_timings)):
            st.markdown(f"**Schedule {i + 1}**")
            col1, col2 = st.columns(2)
            with col1:
                morning_open = st.time_input(f"Morning Opening", key=f"mo_{i}")
                morning_close = st.time_input(f"Morning Closing", key=f"mc_{i}")
            with col2:
                evening_open = st.time_input(f"Evening Opening", key=f"eo_{i}")
                evening_close = st.time_input(f"Evening Closing", key=f"ec_{i}")
            
            timings.append({
                'morningOpening': morning_open.strftime("%I:%M %p"),
                'morningClosing': morning_close.strftime("%I:%M %p"),
                'eveningOpening': evening_open.strftime("%I:%M %p"),
                'eveningClosing': evening_close.strftime("%I:%M %p")
            })
        
        # Images
        st.markdown("### Images")
        uploaded_files = st.file_uploader(
            "Upload temple images",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="You can upload multiple images"
        )
        
        # Process uploaded images
        images = []
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Convert to base64
                bytes_data = uploaded_file.getvalue()
                base64_image = base64.b64encode(bytes_data).decode()
                images.append(f"data:image/{uploaded_file.type.split('/')[-1]};base64,{base64_image}")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button("Add Temple", use_container_width=True)
        
        if submit_button:
            if name and location and description:
                temple_data = {
                    'name': name,
                    'location': location,
                    'description': description,
                    'timings': timings,
                    'images': images
                }
                
                temple_id = create_temple(temple_data)
                if temple_id:
                    st.success("Temple added successfully!")
                    st.session_state.selected_temple = temple_id
                    st.session_state.page = "temple_detail"
                    st.rerun()
                else:
                    st.error("Failed to add temple. Please try again.")
            else:
                st.warning("Please fill in all required fields marked with *")

def show_edit_temple(temple_id: str):
    """Display form to edit an existing temple"""
    st.markdown("## ✏️ Edit Temple")
    
    if not is_admin():
        st.error("Access denied. Admin privileges required.")
        return
    
    temple = get_temple_by_id(temple_id)
    if not temple:
        st.error("Temple not found!")
        return
    
    with st.form("edit_temple_form"):
        # Basic information
        st.markdown("### Basic Information")
        name = st.text_input("Temple Name *", value=temple.get('name', ''))
        location = st.text_input("Location *", value=temple.get('location', ''))
        description = st.text_area("Description *", value=temple.get('description', ''), height=150)
        
        # Timings
        st.markdown("### Timings")
        existing_timings = temple.get('timings', [])
        num_timings = st.number_input(
            "Number of timing schedules",
            min_value=1,
            max_value=5,
            value=len(existing_timings) if existing_timings else 1
        )
        
        timings = []
        for i in range(int(num_timings)):
            st.markdown(f"**Schedule {i + 1}**")
            existing = existing_timings[i] if i < len(existing_timings) else {}
            
            col1, col2 = st.columns(2)
            with col1:
                # Parse existing time or use default
                try:
                    mo_time = datetime.strptime(existing.get('morningOpening', '06:00 AM'), "%I:%M %p").time()
                except:
                    mo_time = datetime.strptime('06:00 AM', "%I:%M %p").time()
                
                try:
                    mc_time = datetime.strptime(existing.get('morningClosing', '12:00 PM'), "%I:%M %p").time()
                except:
                    mc_time = datetime.strptime('12:00 PM', "%I:%M %p").time()
                
                morning_open = st.time_input(f"Morning Opening", value=mo_time, key=f"mo_{i}")
                morning_close = st.time_input(f"Morning Closing", value=mc_time, key=f"mc_{i}")
            
            with col2:
                try:
                    eo_time = datetime.strptime(existing.get('eveningOpening', '04:00 PM'), "%I:%M %p").time()
                except:
                    eo_time = datetime.strptime('04:00 PM', "%I:%M %p").time()
                
                try:
                    ec_time = datetime.strptime(existing.get('eveningClosing', '08:00 PM'), "%I:%M %p").time()
                except:
                    ec_time = datetime.strptime('08:00 PM', "%I:%M %p").time()
                
                evening_open = st.time_input(f"Evening Opening", value=eo_time, key=f"eo_{i}")
                evening_close = st.time_input(f"Evening Closing", value=ec_time, key=f"ec_{i}")
            
            timings.append({
                'morningOpening': morning_open.strftime("%I:%M %p"),
                'morningClosing': morning_close.strftime("%I:%M %p"),
                'eveningOpening': evening_open.strftime("%I:%M %p"),
                'eveningClosing': evening_close.strftime("%I:%M %p")
            })
        
        # Images
        st.markdown("### Images")
        st.info("Current images will be kept. Upload new images to add more.")
        
        # Show existing images
        if temple.get('images'):
            st.markdown("**Current Images:**")
            cols = st.columns(min(len(temple['images']), 3))
            for idx, img in enumerate(temple['images'][:3]):
                with cols[idx]:
                    if img.startswith('data:image'):
                        st.markdown(f"""
                        <img src="{img}" style="width: 100%; height: 100px; object-fit: cover; border-radius: 5px;">
                        """, unsafe_allow_html=True)
                    else:
                        try:
                            st.image(img, use_container_width=True)
                        except:
                            st.text("Image preview unavailable")
        
        uploaded_files = st.file_uploader(
            "Upload additional images",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="These will be added to existing images"
        )
        
        # Process uploaded images
        new_images = []
        if uploaded_files:
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.getvalue()
                base64_image = base64.b64encode(bytes_data).decode()
                new_images.append(f"data:image/{uploaded_file.type.split('/')[-1]};base64,{base64_image}")
        
        # Submit buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state.page = "temple_detail"
                st.rerun()
        with col2:
            submit_button = st.form_submit_button("Update Temple", use_container_width=True, type="primary")
        
        if submit_button:
            if name and location and description:
                # Combine existing and new images
                all_images = temple.get('images', []) + new_images
                
                update_data = {
                    'name': name,
                    'location': location,
                    'description': description,
                    'timings': timings,
                    'images': all_images
                }
                
                if update_temple(temple_id, update_data):
                    st.success("Temple updated successfully!")
                    st.session_state.page = "temple_detail"
                    st.rerun()
                else:
                    st.error("Failed to update temple. Please try again.")
            else:
                st.warning("Please fill in all required fields marked with *")

def show_admin_dashboard():
    """Display admin dashboard with statistics and management options"""
    st.markdown("## 📊 Admin Dashboard")
    
    if not is_admin():
        st.error("Access denied. Admin privileges required.")
        return
    
    # Statistics
    stats = get_temple_stats()
    
    # Display stats in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Temples", stats['total_temples'])
    
    with col2:
        st.metric("Total Users", stats['total_users'])
    
    with col3:
        st.metric("Admin Users", stats['admin_users'])
    
    with col4:
        st.metric("Regular Users", stats['total_users'] - stats['admin_users'])
    
    st.markdown("---")
    
    # Temples by location chart
    if stats['temples_by_location']:
        st.markdown("### Temples by Location")
        locations = [item['_id'] for item in stats['temples_by_location']]
        counts = [item['count'] for item in stats['temples_by_location']]
        
        import plotly.express as px
        fig = px.bar(x=locations, y=counts, labels={'x': 'Location', 'y': 'Number of Temples'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Quick Actions
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add New Temple", use_container_width=True):
            st.session_state.page = "add_temple"
            st.rerun()
    
    with col2:
        if st.button("🛕 View All Temples", use_container_width=True):
            st.session_state.page = "temples"
            st.rerun()
    
    with col3:
        if st.button("👥 Manage Users", use_container_width=True):
            st.session_state.show_users = True
    
    # User Management Section
    if st.session_state.get('show_users', False):
        st.markdown("---")
        st.markdown("### User Management")
        
        users = get_all_users()
        if users:
            # Create a table of users
            user_data = []
            for user in users:
                user_data.append({
                    'Name': user.get('name', 'N/A'),
                    'Email': user.get('email', 'N/A'),
                    'Role': user.get('role', 'user').title(),
                    'Created': str(user.get('created_at', 'N/A'))[:10]
                })
            
            import pandas as pd
            df = pd.DataFrame(user_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No users found")
    
    # Recent Temples
    st.markdown("---")
    st.markdown("### Recent Temples")
    temples = get_all_temples()
    recent_temples = sorted(temples, key=lambda x: x.get('created_at', datetime.min), reverse=True)[:5]
    
    if recent_temples:
        for temple in recent_temples:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**{temple.get('name', 'Unknown')}**")
            with col2:
                st.markdown(f"📍 {temple.get('location', 'Unknown')}")
            with col3:
                if st.button("View", key=f"view_admin_{temple['_id']}"):
                    st.session_state.selected_temple = temple['_id']
                    st.session_state.page = "temple_detail"
                    st.rerun()
    else:
        st.info("No temples added yet")
