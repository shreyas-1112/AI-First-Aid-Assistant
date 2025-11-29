"""
Upload box component for image upload
"""
import streamlit as st
from typing import Optional
import os


def render_upload_box():
    """Render file upload component"""
    st.markdown("### 📸 Upload Injury Image")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("ℹ️ Supported formats: JPG, PNG, GIF, WebP")
        st.caption("Max size: 10 MB")
    
    with col2:
        st.warning("⚠️ This is not a substitute for medical professionals")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png", "gif", "webp"],
        key="injury_image"
    )
    
    return uploaded_file


def save_uploaded_file(uploaded_file) -> Optional[str]:
    """
    Save uploaded file and return path
    
    Args:
        uploaded_file: Streamlit uploaded file
    
    Returns:
        Path to saved file or None
    """
    if uploaded_file is None:
        return None
    
    # Create temp directory if it doesn't exist
    os.makedirs("temp", exist_ok=True)
    
    # Save file
    file_path = os.path.join("temp", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path


def display_uploaded_image(uploaded_file):
    """
    Display uploaded image
    
    Args:
        uploaded_file: Streamlit uploaded file
    """
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
