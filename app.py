"""
Main Streamlit Frontend Application for AI First Aid Assistant
"""
import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import components
from frontend.components import (
    upload_box, panic_mode, audio_player, result_cards, 
    warning_box, doctor_box, voice_input, hospital_locator
)
from frontend.utils.api_client import APIClient
from config.languages import LANGUAGES, get_translation
from backend.services.hospital_locator import HospitalLocator

# Page configuration
st.set_page_config(
    page_title="AI First Aid Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        border-radius: 10px;
        padding: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "emergency_mode" not in st.session_state:
    st.session_state.emergency_mode = False

if "language" not in st.session_state:
    st.session_state.language = "en"


def get_text(key: str) -> str:
    """Get translated text for current language"""
    return get_translation(st.session_state.language, key)


def main():
    """Main application function"""
    
    # Language Switcher in Top Right
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col3:
        language_option = st.selectbox(
            "🌐 Language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x],
            key="lang_selector",
            index=list(LANGUAGES.keys()).index(st.session_state.language)
        )
        if language_option != st.session_state.language:
            st.session_state.language = language_option
            st.rerun()
    
    # Header
    with col2:
        pass  # Spacer
    
    with col1:
        st.markdown("""
        # 🏥 AI First Aid Assistant
        ### AI-Powered Medical Image Analysis & First Aid Guidance
        """)
    
    st.markdown("---")
    
    # Display disclaimer
    warning_box.display_disclaimer()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select an option:",
        ["📸 Analyze Image", "🗣️ Voice Input", "🏥 Find Doctor", "🚨 Emergency Mode", "📚 Education", "ℹ️ About"]
    )
    
    # Check backend connectivity
    if not st.session_state.api_client.health_check():
        st.error("""
        ⚠️ **Backend Connection Error**
        
        The backend API is not responding. Make sure it's running:
        ```
        python -m backend.main
        ```
        """)
        return
    
    if page == "📸 Analyze Image":
        analyze_image_page()
    elif page == "🗣️ Voice Input":
        voice_input_page()
    elif page == "🏥 Find Doctor":
        find_doctor_page()
    elif page == "🚨 Emergency Mode":
        emergency_mode_page()
    elif page == "📚 Education":
        education_page()
    else:
        about_page()


def analyze_image_page():
    """Image analysis page"""
    st.markdown("## 📸 Injury Image Analysis")
    
    # Display safety warning
    warning_box.display_safety_warning()
    warning_box.display_limitation_notice()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Step 1: Upload Image")
        uploaded_file = upload_box.render_upload_box()
        
        if uploaded_file is not None:
            # Display uploaded image
            upload_box.display_uploaded_image(uploaded_file)
            
            # Save file
            image_path = upload_box.save_uploaded_file(uploaded_file)
            
            # Step 2: Patient Information
            st.markdown("### Step 2: Patient Information")
            medical_info = doctor_box.display_medical_history_form()
            
            # Step 3: Analyze
            st.markdown("### Step 3: Analyze")
            
            if st.button("🔍 Analyze Image", width='stretch', type="primary"):
                with st.spinner("Analyzing image... This may take a moment..."):
                    try:
                        result = st.session_state.api_client.upload_image(
                            image_path,
                            age_group=medical_info["age_group"]
                        )
                        
                        if "error" in result:
                            st.error(f"Analysis Error: {result['error']}")
                        else:
                            st.session_state.analysis_result = result
                            st.success("✅ Analysis Complete!")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("### 📋 Quick Reference")
        st.info("""
        **Severity Levels:**
        - 🟢 Mild: Minor injury
        - 🟡 Moderate: Noticeable injury
        - 🔴 Severe: Serious injury
        
        **Remember:**
        - Always verify with professionals
        - Don't delay seeking medical help
        - Stay calm and follow instructions
        """)
    
    # Display results
    if st.session_state.analysis_result:
        st.markdown("---")
        display_analysis_results(st.session_state.analysis_result)


def display_analysis_results(result):
    """Display analysis results"""
    if "data" in result:
        data = result["data"]
        
        # Injury analysis card
        result_cards.display_injury_analysis_card(data)
        
        # Emergency alert
        result_cards.display_emergency_alert(data.get("is_emergency", False))
        
        # First aid steps
        if "first_aid_steps" in data:
            result_cards.display_first_aid_steps(data["first_aid_steps"])
        
        # Audio guidance
        col1, col2 = st.columns([3, 1])
        with col1:
            if audio_player.generate_audio_button():
                st.info("🔊 Audio feature requires pyttsx3 installation")
        
        # Professional help
        if "professional_help" in data:
            result_cards.display_professional_help(data["professional_help"])
        
        # Age guidance
        if "age_guidance" in data:
            result_cards.display_age_guidance(data.get("age_group", "Unknown"), data["age_guidance"])
        
        # Get prevention tips
        injury_type = data.get("injury_type", "")
        if injury_type and st.button("Get Prevention Tips", key="get_tips"):
            tips_result = st.session_state.api_client.get_prevention_tips(injury_type)
            if "data" in tips_result:
                result_cards.display_prevention_tips(tips_result["data"].get("prevention_tips", []))
        
        # Doctor recommendation
        st.markdown("---")
        doctor_box.display_doctor_recommendation()
        doctor_box.display_specialist_recommendation(
            data.get("injury_type", ""),
            data.get("severity", "")
        )
        doctor_box.display_follow_up_care(data.get("injury_type", ""))


def voice_input_page():
    """Voice input page for describing injuries"""
    st.markdown(f"## 🗣️ {get_text('voice_input')}")
    
    warning_box.display_safety_warning()
    
    st.markdown(f"""
    ### {get_text('record_description')}
    
    - 🎤 {get_text('record')}
    - 📁 {get_text('upload')}
    - 📝 {get_text('type')}
    """)
    
    # Initialize voice input state
    if "voice_action_selected" not in st.session_state:
        st.session_state.voice_action_selected = None
    if "voice_data_confirmed" not in st.session_state:
        st.session_state.voice_data_confirmed = None
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {get_text('quick_actions')}")
        
        # If no action selected yet, show quick actions
        if st.session_state.voice_action_selected is None:
            col_buttons1, col_buttons2, col_buttons3, col_buttons4 = st.columns(4)
            
            with col_buttons1:
                if st.button("🔴 I'm in Emergency!", key="emergency_voice_new", width='stretch'):
                    st.session_state.voice_action_selected = "emergency"
                    st.rerun()
            
            with col_buttons2:
                if st.button("🎤 Record Injury", key="record_injury_new", width='stretch'):
                    st.session_state.voice_action_selected = "record"
                    st.rerun()
            
            with col_buttons3:
                if st.button("📝 Type Instead", key="type_injury_new", width='stretch'):
                    st.session_state.voice_action_selected = "type"
                    st.rerun()
            
            with col_buttons4:
                if st.button("📁 Upload Audio", key="upload_audio_main_new", width='stretch'):
                    st.session_state.voice_action_selected = "upload"
                    st.rerun()
        
        # If recording action selected, show recording interface
        if st.session_state.voice_action_selected == "record":
            st.markdown("---")
            voice_data = voice_input.display_voice_injury_form()
            
            # If voice data is confirmed, display results
            if voice_data and voice_data.get("confirmed"):
                st.session_state.voice_data_confirmed = voice_data
                st.session_state.voice_action_selected = "results"
                st.rerun()
        
        # If results should be shown
        if st.session_state.voice_action_selected == "results" and st.session_state.voice_data_confirmed:
            voice_data = st.session_state.voice_data_confirmed
            
            st.success("✅ Voice input received and analyzed!")
            
            st.markdown("---")
            st.markdown("### 📋 Injury Information")
            
            # Process the voice input
            if voice_data.get("is_emergency"):
                st.error(get_text('emergency_detected'))
                col_emergency1, col_emergency2 = st.columns(2)
                with col_emergency1:
                    if st.button(get_text('call_911'), width='stretch', type="primary"):
                        st.error(get_text('please_call_911'))
                with col_emergency2:
                    if st.button(get_text('get_emergency_guidance'), width='stretch'):
                        injury_type = voice_data.get("injury_type", get_text('unknown'))
                        guidance = st.session_state.api_client.get_emergency_guidance(injury_type)
                        if "data" in guidance:
                            st.info(f"📋 {get_text('emergency_guidance')}:")
                            for step in guidance["data"].get("steps", []):
                                st.write(f"• {step}")
            
            # Show analysis
            col_analysis1, col_analysis2, col_analysis3 = st.columns(3)
            with col_analysis1:
                st.metric(get_text('injury_type'), voice_data.get("injury_type", get_text('unknown')))
            with col_analysis2:
                st.metric(get_text('severity'), voice_data.get("severity", get_text('not_specified')))
            with col_analysis3:
                status = "🚨 EMERGENCY" if voice_data.get("is_emergency") else "Standard"
                st.metric(get_text('status'), status)
            
            if voice_data.get("body_area"):
                st.info(f"{get_text('affected_area')}: {voice_data.get('body_area')}")
            
            # Show first aid guidance
            st.markdown("---")
            st.markdown(f"### {get_text('first_aid_guidance')}")
            
            with st.spinner(get_text('getting_guidance')):
                # Ensure severity has a valid value
                injury_type = voice_data.get("injury_type", get_text('unknown'))
                severity = voice_data.get("severity") or "Moderate"
                affected_area = voice_data.get("body_area")
                
                print(f"[DEBUG] Requesting guidance: injury_type={injury_type}, severity={severity}, area={affected_area}")
                
                guidance = st.session_state.api_client.get_first_aid_guidance(
                    injury_type=injury_type,
                    severity=severity,
                    affected_area=affected_area
                )
                
                print(f"[DEBUG] Guidance response: {guidance}")
                
                # Check for errors in response
                if isinstance(guidance, dict):
                    if "error" in guidance or guidance.get("status") == "error":
                        error_msg = get_text('unknown')
                        if isinstance(guidance.get("error"), dict):
                            error_msg = guidance.get("error", {}).get("message", get_text('unknown'))
                        elif isinstance(guidance.get("error"), str):
                            error_msg = guidance.get("error")
                        st.error(f"{get_text('error_getting_guidance')}: {error_msg}")
                    elif "data" in guidance:
                        data = guidance["data"]
                        
                        # Display first aid steps
                        if "first_aid_steps" in data and data["first_aid_steps"]:
                            st.markdown(f"#### {get_text('steps_follow')}")
                            for step in data["first_aid_steps"]:
                                # Handle both dict and string formats
                                if isinstance(step, dict):
                                    st.markdown(f"**{get_text('step')} {step.get('order', '?')}:** {step.get('title', '')}")
                                    st.write(step.get('description', ''))
                                    if step.get('warning'):
                                        st.warning(f"{get_text('warning')} {step.get('warning')}")
                                    if step.get('duration'):
                                        st.caption(f"{get_text('duration')}: {step.get('duration')}")
                                else:
                                    st.markdown(f"• {step}")
                            st.markdown("")
                        else:
                            st.warning(get_text('no_steps_available'))
                        
                        # Display professional help recommendation
                        if "professional_help" in data and data["professional_help"]:
                            st.info(f"{get_text('professional_help')}\n{data['professional_help']}")
                    else:
                        st.error(get_text('unexpected_format'))
                else:
                    st.error(f"{get_text('error_getting_guidance')}: {guidance}")
            
            # Show nearby hospitals
            st.markdown("---")
            st.markdown(f"### {get_text('find_hospitals')}")
            
            hospital_locator.display_hospital_locator()
            
            # Reset buttons
            col_reset1, col_reset2 = st.columns(2)
            with col_reset1:
                if st.button(get_text('record_another'), width='stretch'):
                    st.session_state.voice_action_selected = None
                    st.session_state.voice_data_confirmed = None
                    st.rerun()
            
            with col_reset2:
                if st.button(get_text('back_to_menu'), width='stretch'):
                    st.session_state.voice_action_selected = None
                    st.session_state.voice_data_confirmed = None
                    st.rerun()
        
        elif st.session_state.voice_action_selected == "type":
            st.markdown("---")
            text_desc = st.text_area(
                "Describe your injury:",
                placeholder="E.g., 'I burned my hand on the stove'",
                height=150,
                key="voice_type_textarea"
            )
            
            if text_desc:
                injury_type = voice_input.extract_injury_type(text_desc)
                severity = voice_input.extract_severity(text_desc)
                is_emergency = voice_input.detect_emergency(text_desc)
                body_area = voice_input.extract_body_area(text_desc)
                
                st.markdown("---")
                st.markdown("### 📋 Analysis")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Injury Type", injury_type or "Unknown")
                with col2:
                    st.metric("Severity", severity or "Not specified")
                with col3:
                    status = "🚨 EMERGENCY" if is_emergency else "Standard"
                    st.metric("Status", status)
                
                if body_area:
                    st.info(f"📍 Affected Area: {body_area}")
                
                if is_emergency:
                    st.error("🚨 EMERGENCY DETECTED!")
                
                if st.button("Get First Aid Guidance", width='stretch', type="primary"):
                    with st.spinner("Getting first aid guidance..."):
                        guidance = st.session_state.api_client.get_first_aid_guidance(
                            injury_type=injury_type or "Unknown",
                            severity=severity or "Moderate",
                            affected_area=body_area
                        )
                        
                        if "data" in guidance:
                            data = guidance["data"]
                            
                            st.markdown("---")
                            st.markdown("### 🏥 First Aid Guidance")
                            
                            if "first_aid_steps" in data:
                                for i, step in enumerate(data["first_aid_steps"], 1):
                                    st.markdown(f"**Step {i}:** {step}")
        
        elif st.session_state.voice_action_selected == "emergency":
            st.error("🚨 EMERGENCY MODE ACTIVATED")
            st.write("Contacting emergency services...")
            
            if st.button("☎️ CALL 911", width='stretch', type="primary"):
                st.error("⚠️ Please call 911 immediately!")
            
            if st.button("🔙 Go Back", width='stretch'):
                st.session_state.voice_action_selected = None
                st.rerun()
        
        elif st.session_state.voice_action_selected == "upload":
            st.markdown("---")
            uploaded_file = upload_box.render_upload_box()
            if uploaded_file:
                upload_box.display_uploaded_image(uploaded_file)
                st.success("Image uploaded. Proceeding to analysis...")
            
            if st.button("🔙 Go Back", width='stretch'):
                st.session_state.voice_action_selected = None
                st.rerun()
    
    with col2:
        st.markdown("### 💡 Tips")
        st.info("""
        **For Best Results:**
        - Speak clearly
        - Describe location of injury
        - Mention when it happened
        - Note any symptoms
        - Be specific about severity
        """)


def find_doctor_page():
    """Find Doctor/Specialists page"""
    st.markdown(f"## 🏥 {get_text('find_doctors')}")
    
    st.write(get_text('enter_location'))
    
    # Initialize session state for search
    if "doctor_search_address" not in st.session_state:
        st.session_state.doctor_search_address = None
    if "doctor_search_radius" not in st.session_state:
        st.session_state.doctor_search_radius = 5
    
    # Form for doctor search
    with st.form("find_doctor_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            address = st.text_input(
                f"{get_text('find_doctors')}:",
                placeholder="e.g., 123 Main St, City, State or 12345",
                key="doctor_address_input"
            )
        
        with col2:
            radius = st.slider(
                get_text('search_radius'),
                min_value=1,
                max_value=50,
                value=5,
                step=1,
                key="doctor_radius_slider"
            )
        
        submitted = st.form_submit_button("🔍 " + get_text('find_doctors'), type="primary")
        
        if submitted and address:
            st.session_state.doctor_search_address = address
            st.session_state.doctor_search_radius = radius
    
    # Display results if search was performed
    if st.session_state.doctor_search_address:
        with st.spinner(get_text('finding_hospitals')):
            try:
                locator = HospitalLocator()
                
                # Get coordinates from address
                coords = locator.get_address_coordinates(st.session_state.doctor_search_address)
                if coords:
                    lat, lon = coords
                    
                    # Get hospitals/clinics near the location
                    hospitals = locator.get_hospitals_near_location(lat, lon, radius_km=st.session_state.doctor_search_radius)
                    
                    if hospitals:
                        st.markdown(f"### 🏥 {get_text('nearby_facilities')}")
                        st.markdown(f"✅ {get_text('hospitals_found')} **{len(hospitals)}** {get_text('facilities')}:")
                        
                        # Display doctors/specialists
                        for idx, hospital in enumerate(hospitals, 1):
                            with st.expander(
                                f"**{idx}. {hospital.get('name', get_text('unknown'))}** - {hospital.get('distance_km', 'N/A')} {get_text('km_away')}",
                                expanded=(idx == 1)
                            ):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    if hospital.get('type'):
                                        st.markdown(f"**{get_text('hospital_type')}:** {hospital.get('type')}")
                                    st.markdown(f"**{get_text('hospital_distance')}:** {hospital.get('distance_km', 'N/A')} km")
                                    
                                    if hospital.get('phone'):
                                        st.markdown(f"**{get_text('hospital_phone')}** {hospital.get('phone')}")
                                    
                                    if hospital.get('opening_hours'):
                                        st.markdown(f"**{get_text('hospital_hours')}** {hospital.get('opening_hours')}")
                                    
                                    if hospital.get('operator'):
                                        st.markdown(f"**{get_text('hospital_organization')}:** {hospital.get('operator')}")
                                    
                                    if hospital.get('website'):
                                        st.markdown(f"**{get_text('hospital_website')}** [{hospital.get('website')}]({hospital.get('website')})")
                                
                                with col2:
                                    col_map, col_nav = st.columns(2)
                                    
                                    with col_map:
                                        if st.button(
                                            get_text('hospital_map'),
                                            key=f"doc_map_{idx}",
                                            width='stretch'
                                        ):
                                            st.write(f"[Open in Google Maps]({hospital.get('google_maps_url')})")
                                    
                                    with col_nav:
                                        if st.button(
                                            get_text('hospital_navigate'),
                                            key=f"doc_nav_{idx}",
                                            width='stretch'
                                        ):
                                            st.write(f"[Open Navigation]({hospital.get('osm_url', hospital.get('google_maps_url'))})")
                        
                        # Show map
                        st.markdown("---")
                        st.markdown(f"### {get_text('hospital_map')}")
                        map_data = []
                        for hospital in hospitals:
                            if hospital.get("latitude") and hospital.get("longitude"):
                                map_data.append({
                                    "latitude": float(hospital.get("latitude")),
                                    "longitude": float(hospital.get("longitude")),
                                })
                        
                        if map_data:
                            st.map(map_data, zoom=12, use_container_width=True)
                            st.caption("🔴 Red pins show doctor/specialist locations")
                    else:
                        st.warning(get_text('no_hospitals_found'))
                else:
                    st.error(f"Could not find coordinates for address: {st.session_state.doctor_search_address}")
                    
            except Exception as e:
                st.error(f"Error finding doctors: {str(e)}")
        
        # Clear search button
        if st.button("🔄 New Search"):
            st.session_state.doctor_search_address = None
            st.session_state.doctor_search_radius = 5
            st.rerun()



def emergency_mode_page():
    """Emergency mode page"""
    st.markdown("## 🚨 Emergency Mode")
    
    warning_box.display_safety_warning()
    
    st.markdown("""
    ### Are you in an Emergency?
    
    If you are experiencing a **life-threatening emergency**, please:
    
    1. **CALL 108 IMMEDIATELY** - Do not wait
    2. Follow emergency dispatcher instructions
    3. Use this app for reference only while waiting for help
    """)
    
    # Display panic mode
    panic_mode.display_panic_mode()
    
    # Get emergency info
    injury_type = panic_mode.get_emergency_injury_type()
    
    if injury_type:
        with st.spinner("Getting emergency guidance..."):
            guidance = st.session_state.api_client.get_emergency_guidance(injury_type)
            
            if "data" in guidance:
                emergency_info = guidance["data"]
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### Emergency Instructions")
                    
                    if "steps" in emergency_info:
                        for i, step in enumerate(emergency_info["steps"], 1):
                            st.markdown(f"**{i}. {step}**")
                    
                    if "do_not" in emergency_info:
                        st.error("### Do NOT:")
                        for item in emergency_info["do_not"]:
                            st.write(f"❌ {item}")
                
                with col2:
                    st.metric("Emergency Number", "911")
                    st.info("Remember: Professionals are trained to help.\nFollow their guidance.")


def education_page():
    """Education and resources page"""
    st.markdown("## 📚 First Aid Education")
    
    st.markdown("""
    ### Learn First Aid Skills
    
    This app provides guidance, but proper training is essential.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🏥 CPR & First Aid Training
        - American Red Cross
        - American Heart Association
        - Local hospitals and community centers
        
        [Find a Course Near You](https://www.redcross.org/take-a-class)
        """)
    
    with col2:
        st.markdown("""
        ### 📖 Injury Types
        - Cuts and Wounds
        - Burns
        - Fractures
        - Head Injuries
        - Shock
        - Allergic Reactions
        """)
    
    with col3:
        st.markdown("""
        ### 🔗 Resources
        - Mayo Clinic First Aid
        - WebMD Health
        - CDC Safety Information
        - WHO Emergency Care
        """)
    
    st.markdown("---")
    
    # Common injuries
    st.markdown("### Common Injuries Overview")
    
    injury_info = {
        "Cuts": "Minor cuts usually stop bleeding in 10-15 minutes. Apply pressure and clean with soap and water.",
        "Burns": "Cool with water for 15-20 minutes, do not pop blisters.",
        "Sprains": "Rest, Ice, Compression, Elevation (RICE protocol)",
        "Fractures": "Immobilize and seek professional medical help immediately",
    }
    
    for injury, info in injury_info.items():
        with st.expander(f"ℹ️ {injury}"):
            st.write(info)


def about_page():
    """About page"""
    st.markdown("## ℹ️ About AI First Aid Assistant")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Mission
        
        Provide quick, accessible first aid guidance using AI technology
        to assist in emergency situations and promote first aid awareness.
        
        ### 🔬 Technology
        
        - **AI Model**: Google Gemini 1.5 Vision
        - **Backend**: FastAPI
        - **Frontend**: Streamlit
        - **Language**: Python 3.9+
        """)
    
    with col2:
        st.markdown("""
        ### ⚠️ Important Disclaimer
        
        This application:
        - Provides **GENERAL GUIDANCE ONLY**
        - Is **NOT a substitute** for professional medical advice
        - Should **NOT replace** emergency services
        - Requires **VERIFICATION by healthcare professionals**
        
        **Always consult with qualified medical professionals.**
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📞 Emergency Numbers
    
    - **Emergency**:108
    - **Poison Control**: 080-2341710
    - **Crisis Hotline**: 112 or 100
    - **Non-Emergency**: Call your local police department
    """)
    
    st.markdown("""
    ### 🔒 Privacy & Security
    
    - Images are processed temporarily and not permanently stored
    - No personal information is retained
    - For sensitive medical data, use professional medical services
    - This is a demonstration application
    """)


if __name__ == "__main__":
    main()
