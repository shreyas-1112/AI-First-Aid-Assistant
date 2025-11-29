"""
Warning box component for alerts and notices
"""
import streamlit as st


def display_disclaimer():
    """Display medical disclaimer"""
    with st.sidebar:
        st.markdown("---")
        st.warning("""
        ### ⚠️ MEDICAL DISCLAIMER
        
        This application provides general first aid guidance only.
        
        It is NOT a substitute for professional medical advice, 
        diagnosis, or treatment.
        
        **Always consult with qualified healthcare professionals.**
        
        In case of emergency, call 911 immediately.
        """)


def display_safety_warning():
    """Display safety warning"""
    st.warning("""
    ### ⚠️ IMPORTANT SAFETY NOTICE
    
    - Use this app for informational purposes only
    - Always follow guidance from medical professionals
    - Call emergency services (911) for life-threatening situations
    - Do not attempt procedures you're not trained for
    - Keep emergency numbers readily available
    """)


def display_privacy_notice():
    """Display privacy notice"""
    with st.expander("🔒 Privacy & Data Notice"):
        st.markdown("""
        - Your image is analyzed and stored temporarily for processing
        - We do not store personally identifiable information
        - For HIPAA compliance and medical data protection, consult professional medical services
        - This is a demonstration application, not for production medical use
        """)


def display_limitation_notice():
    """Display application limitations"""
    st.info("""
    ### ℹ️ Application Limitations
    
    - Works best with clear, well-lit injury images
    - May not identify all types of injuries
    - Age detection is approximate based on visual indicators
    - Results should be verified by medical professionals
    - Network connectivity required for full functionality
    """)


def display_status_banner(status: str):
    """
    Display status banner
    
    Args:
        status: Status message
    """
    if status == "loading":
        st.warning("⏳ Processing... Please wait")
    elif status == "error":
        st.error("❌ An error occurred. Please try again.")
    elif status == "success":
        st.success("✅ Analysis complete")
