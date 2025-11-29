"""
Panic mode component for emergencies
"""
import streamlit as st


def render_panic_mode_button():
    """Render panic mode button"""
    st.markdown("---")
    
    # Create a red alert for panic mode
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(
            "🚨 EMERGENCY MODE 🚨",
            key="panic_mode",
            use_container_width=True,
            help="Click if this is a life-threatening emergency"
        ):
            return True
    
    return False


def display_panic_mode():
    """Display panic mode content"""
    st.markdown("---")
    st.error("""
    ### 🚨 EMERGENCY MODE ACTIVATED 🚨
    
    **CALL 911 IMMEDIATELY**
    
    This app provides guidance only and is NOT a substitute for emergency services.
    
    **Do not delay calling emergency services while using this app.**
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Emergency Number", "911", help="Call immediately for life-threatening situations")
    
    with col2:
        st.metric("Poison Control", "1-800-222-1222", help="For poisoning emergencies")
    
    with col3:
        st.metric("Crisis Hotline", "988", help="Mental health crisis support")
    
    st.markdown("""
    ### Emergency Instructions:
    1. **CALL 911** or your local emergency number
    2. **Stay calm** and provide clear information
    3. **Follow dispatcher instructions**
    4. **Do not hang up** until instructed
    5. **Provide location**, nature of emergency, and any relevant medical history
    
    ### While Waiting for Emergency Services:
    - Ensure the person's safety
    - Monitor breathing and consciousness
    - Perform CPR if trained and person is unresponsive
    - Do not move the person unnecessarily
    - Keep them calm and comfortable
    """)
    
    st.markdown("---")


def get_emergency_injury_type():
    """Get injury type in emergency mode"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        injury_type = st.selectbox(
            "What type of emergency?",
            [
                "Severe bleeding",
                "Unconsciousness",
                "Chest pain",
                "Difficulty breathing",
                "Severe burns",
                "Choking",
                "Anaphylaxis/Allergic reaction",
                "Stroke symptoms",
                "Heart attack",
                "Poisoning",
                "Other"
            ]
        )
    
    with col2:
        st.caption("")  # Spacing
        if st.button("Get Help", key="emergency_help"):
            return injury_type
    
    return None
