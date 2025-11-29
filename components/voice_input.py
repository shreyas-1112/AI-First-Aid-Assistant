"""
Voice Input Component - Capture voice input for injury description
"""
import streamlit as st
import os
import tempfile
from typing import Optional, Dict, Any
from config.languages import get_translation


def get_text(key: str) -> str:
    """Get translated text for current language"""
    language = st.session_state.get("language", "en")
    return get_translation(language, key)


def display_voice_quick_action() -> Optional[str]:
    """Display quick action buttons for voice input"""
    st.markdown(f"### {get_text('quick_actions')}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(get_text('emergency_button'), key="emergency_voice", use_container_width=True):
            return "emergency"
    
    with col2:
        if st.button(get_text('record_injury'), key="record_injury", use_container_width=True):
            return "record"
    
    with col3:
        if st.button(get_text('type_injury'), key="type_injury", use_container_width=True):
            return "type"
    
    with col4:
        if st.button(get_text('upload_audio'), key="upload_audio_main", use_container_width=True):
            return "upload"
    
    return None


def display_voice_injury_form() -> Optional[Dict[str, Any]]:
    """
    Display form for voice-based injury input
    
    Returns:
        Dictionary with voice input data or None
    """
    # Initialize session state for voice processing
    if "voice_transcription" not in st.session_state:
        st.session_state.voice_transcription = None
    if "voice_processed" not in st.session_state:
        st.session_state.voice_processed = False
    
    st.markdown(f"## 🎤 {get_text('voice_input_title')}")
    st.info(get_text('record_description'))
    
    # Recording section
    st.markdown(f"### {get_text('record_injury')}")
    st.markdown(get_text('record_description'))
    
    audio_data = st.audio_input(f"🎤 {get_text('record')}", key="voice_record_input")
    
    if audio_data is not None:
        st.success(f"✅ {get_text('transcription_complete')}")
        
        # Process the recorded audio
        if not st.session_state.voice_processed:
            with st.spinner(f"🔄 {get_text('transcribing')}"):
                transcription = process_audio(audio_data)
                
                if transcription:
                    st.session_state.voice_transcription = transcription
                    st.session_state.voice_processed = True
                    st.rerun()
    
    # Check if we have processed transcription
    if st.session_state.voice_transcription:
        return display_transcription_results(st.session_state.voice_transcription)
    
    # Upload section
    st.markdown("---")
    st.markdown(f"### {get_text('upload_audio')}")
    st.markdown("Upload an existing audio file (MP3, WAV, M4A, OGG)")
    
    uploaded_file = st.file_uploader(
        f"📁 {get_text('upload')}",
        type=["mp3", "wav", "m4a", "ogg", "flac"],
        key="audio_file_upload"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ {get_text('image_uploaded')}: {uploaded_file.name}")
        
        if not st.session_state.voice_processed:
            # Save uploaded file temporarily and process
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                tmp_path = tmp_file.name
            
            try:
                with st.spinner(f"🔄 {get_text('transcribing')}"):
                    transcription = process_audio_file(tmp_path)
                    
                    if transcription:
                        st.session_state.voice_transcription = transcription
                        st.session_state.voice_processed = True
                        st.rerun()
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
    
    # Text input fallback
    st.markdown("---")
    st.markdown(f"### {get_text('type_injury')}")
    st.markdown("If recording doesn't work, you can type instead")
    
    text_input = st.text_area(
        f"📝 {get_text('injury_type')}:",
        placeholder="E.g., 'I burned my hand on the stove about 5 minutes ago. It's red and hurts a lot.'",
        height=120,
        key="injury_text_input"
    )
    
    if text_input and len(text_input.strip()) > 0:
        st.success(f"✅ {get_text('transcription_complete')}")
        if not st.session_state.voice_processed:
            st.session_state.voice_transcription = text_input
            st.session_state.voice_processed = True
            st.rerun()
    
    return None


def display_transcription_results(text: str) -> Optional[Dict[str, Any]]:
    """
    Display transcription results and get user confirmation
    
    Args:
        text: Transcribed or typed text
    
    Returns:
        Dictionary with extracted injury information if confirmed, None otherwise
    """
    st.markdown("---")
    st.markdown(f"### 📋 {get_text('analysis')}")
    
    injury_type = extract_injury_type(text)
    severity = extract_severity(text)
    is_emergency = detect_emergency(text)
    body_area = extract_body_area(text)
    
    # Display detected information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(get_text('injury_type'), injury_type or get_text('unknown'))
    
    with col2:
        st.metric(get_text('severity'), severity or get_text('not_specified'))
    
    with col3:
        status = "🚨 EMERGENCY" if is_emergency else get_text('normal')
        st.metric(get_text('status'), status)
    
    if body_area:
        st.info(f"{get_text('affected_area')}: {body_area}")
    
    # Show full transcription
    with st.expander(get_text('transcription')):
        st.write(text)
    
    st.markdown("---")
    st.markdown(f"### {get_text('confirm_proceed')}")
    
    # Confirmation buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(get_text('confirm'), key="confirm_proceed_injury", use_container_width=True, type="primary"):
            # Clear session state for next use
            st.session_state.voice_transcription = None
            st.session_state.voice_processed = False
            
            return {
                "transcription": text,
                "injury_type": injury_type,
                "severity": severity,
                "is_emergency": is_emergency,
                "body_area": body_area,
                "confirmed": True
            }
    
    with col2:
        if st.button(get_text('retry'), key="retry_voice_again", use_container_width=True):
            st.session_state.voice_transcription = None
            st.session_state.voice_processed = False
            st.rerun()
    
    with col3:
        if st.button(get_text('cancel'), key="cancel_voice_input", use_container_width=True):
            st.session_state.voice_transcription = None
            st.session_state.voice_processed = False
            st.rerun()
    
    return None


def process_audio(audio_data) -> Optional[str]:
    """
    Process recorded audio and transcribe
    
    Args:
        audio_data: Audio bytes from Streamlit audio_input
    
    Returns:
        Transcribed text or None
    """
    try:
        # Save audio data to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_data.getbuffer())
            tmp_path = tmp_file.name
        
        try:
            transcription = process_audio_file(tmp_path)
            return transcription
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        st.error(f"❌ Error processing audio: {str(e)}")
        return None


def process_audio_file(file_path: str) -> Optional[str]:
    """
    Transcribe audio file using SpeechRecognition
    
    Args:
        file_path: Path to audio file
    
    Returns:
        Transcribed text or None
    """
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 3000
        recognizer.dynamic_energy_threshold = True
        
        try:
            # Load audio file
            audio = sr.AudioFile(file_path)
            
            with audio as source:
                st.info("🔄 Transcribing audio...")
                
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record audio from file
                audio_data = recognizer.record(source)
            
            # Recognize using Google Speech Recognition
            text = recognizer.recognize_google(audio_data, language='en-US')
            st.success("✅ Transcription complete!")
            return text
        
        except sr.RequestError as e:
            st.error(f"❌ Could not connect to speech recognition service: {str(e)}")
            st.info("ℹ️ Make sure you have an internet connection")
            return None
        except sr.UnknownValueError:
            st.error("❌ Could not understand audio. Please speak more clearly and try again.")
            return None
        except Exception as e:
            st.error(f"❌ Error during transcription: {str(e)}")
            return None
    
    except ImportError:
        st.error("❌ Speech recognition library not installed")
        st.info("Install with: pip install SpeechRecognition pyaudio")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


def process_transcription(text: str) -> Dict[str, Any]:
    """
    Process transcribed text and extract injury information
    
    Args:
        text: Transcribed or typed text
    
    Returns:
        Dictionary with extracted injury information
    """
    st.markdown("---")
    st.markdown("### 📋 Detected Information")
    
    injury_type = extract_injury_type(text)
    severity = extract_severity(text)
    is_emergency = detect_emergency(text)
    body_area = extract_body_area(text)
    
    # Display detected information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Injury Type", injury_type or "Unknown")
    
    with col2:
        st.metric("Severity", severity or "Not specified")
    
    with col3:
        status = "🚨 EMERGENCY" if is_emergency else "Normal"
        st.metric("Status", status)
    
    if body_area:
        st.info(f"📍 Affected Area: {body_area}")
    
    st.markdown("---")
    
    # Show full transcription
    with st.expander("📄 Full Transcription"):
        st.write(text)
    
    st.markdown("---")
    
    # Confirmation buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Confirm & Proceed", key="confirm_injury_proceed", use_container_width=True, type="primary"):
            return {
                "transcription": text,
                "injury_type": injury_type,
                "severity": severity,
                "is_emergency": is_emergency,
                "body_area": body_area,
                "confirmed": True
            }
    
    with col2:
        if st.button("🔄 Try Again", key="retry_voice_input", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("⚙️ Skip", key="skip_voice_input", use_container_width=True):
            return {"confirmed": False}
    
    return {}


def extract_injury_type(text: str) -> Optional[str]:
    """Extract injury type from text"""
    if not text:
        return "General Injury"  # Default value
    
    text_lower = text.lower()
    
    injury_keywords = {
        "Cuts and Wounds": ["cut", "wound", "bleeding", "laceration", "slice", "gash", "slash"],
        "Burns": ["burn", "burnt", "scorched", "heat", "fire", "hot", "scalded"],
        "Fractures": ["fracture", "broken", "break", "crack", "snapped", "fractured"],
        "Head Injury": ["head", "concussion", "impact", "knocked", "hit head", "brain"],
        "Shock": ["shock", "shocked", "pale", "weak", "faint"],
        "Allergic Reaction": ["allergy", "allergic", "reaction", "rash", "swelling", "itching"],
        "Severe Bleeding": ["severe bleed", "heavy bleed", "gushing", "hemorrhage", "arterial"],
        "Choking": ["choking", "choke", "can't breath", "stuck", "blocking", "lodged"],
        "Poisoning": ["poison", "toxic", "ingested", "swallowed", "overdose"],
    }
    
    for injury, keywords in injury_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                return injury
    
    return "General Injury"  # Default if no keywords match


def extract_severity(text: str) -> Optional[str]:
    """Extract severity level from text"""
    if not text:
        return "Moderate"  # Default to moderate if cannot determine
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["severe", "very bad", "critical", "emergency", "urgent", "extremely", "seriously", "terrible"]):
        return "Severe"
    elif any(word in text_lower for word in ["moderate", "bad", "significant", "serious", "quite bad", "fairly bad"]):
        return "Moderate"
    elif any(word in text_lower for word in ["mild", "minor", "small", "light", "little", "slight", "barely"]):
        return "Mild"
    
    return "Moderate"  # Default to moderate if cannot determine


def extract_body_area(text: str) -> Optional[str]:
    """Extract body area from text"""
    if not text:
        return None
    
    text_lower = text.lower()
    
    body_areas = [
        "head", "face", "eye", "eyes", "nose", "mouth", "ear", "ears",
        "neck", "shoulder", "shoulders", "arm", "arms", "elbow", "elbows",
        "hand", "hands", "finger", "fingers", "chest", "back", "torso",
        "abdomen", "belly", "stomach", "leg", "legs", "knee", "knees",
        "ankle", "ankles", "foot", "feet", "toe", "toes", "skin", "wrist", "wrists"
    ]
    
    for area in body_areas:
        if area in text_lower:
            return area.capitalize()
    
    return None


def detect_emergency(text: str) -> bool:
    """Detect if text indicates emergency"""
    if not text:
        return False
    
    emergency_keywords = [
        "emergency", "urgent", "critical", "severe", "call 911",
        "unconscious", "not breathing", "no pulse", "bleeding heavily",
        "choking", "poisoned", "overdose", "heart attack", "stroke",
        "unresponsive", "can't breathe", "difficulty breathing", "severe pain",
        "loss of consciousness", "suicidal", "bleeding won't stop"
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in emergency_keywords)


def display_voice_input_button() -> Optional[str]:
    """Legacy function for compatibility"""
    return None


def display_voice_quick_action_old() -> Optional[str]:
    """Legacy function - use display_voice_quick_action instead"""
    return display_voice_quick_action()
