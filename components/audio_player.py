"""
Audio player component
"""
import streamlit as st
import base64
from typing import Optional


def render_audio_player(audio_content: Optional[bytes], label: str = "First Aid Guidance"):
    """
    Render audio player component
    
    Args:
        audio_content: Audio file content in bytes
        label: Label for the audio player
    """
    if audio_content is None:
        return
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.audio(audio_content, format="audio/mp3")
    
    with col2:
        st.caption(label)
        # Download button
        st.download_button(
            label="📥 Download",
            data=audio_content,
            file_name="first_aid_guidance.mp3",
            mime="audio/mp3"
        )


def generate_audio_button() -> bool:
    """Generate button for audio generation"""
    if st.button("🔊 Listen to Guidance", key="generate_audio", use_container_width=True):
        return True
    return False


def display_audio_controls():
    """Display audio control options"""
    st.markdown("### 🔊 Audio Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        speed = st.slider(
            "Speech Speed",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Adjust how fast the audio is read"
        )
    
    with col2:
        volume = st.slider(
            "Volume",
            min_value=0.0,
            max_value=1.0,
            value=0.8,
            step=0.1,
            help="Adjust audio volume"
        )
    
    return speed, volume
