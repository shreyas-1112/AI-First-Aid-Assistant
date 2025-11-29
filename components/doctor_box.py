"""
Doctor box component for professional consultation recommendations
"""
import streamlit as st
import urllib.parse


def display_doctor_recommendation():
    """Display recommendation to consult doctor"""
    st.markdown("### 👨‍⚕ Consult a Medical Professional")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        *This application provides guidance only.*
        
        For proper medical evaluation and treatment:
        - Consult your primary care physician
        - Visit an urgent care clinic
        - Go to the emergency room if necessary
        - Call your local poison control center for poisoning cases
        """)
    
    with col2:
        st.markdown("""
        *Quick Links:*
        
        🏥 [Find Doctor (near me)](https://www.google.com/maps/search/doctor+near+me)
        
        🚑 [Urgent Care](https://www.caregivers.com/)
        
        💊 [Poison Control](https://www.poisonhelp.org/)
        """)


def display_medical_history_form():
    """Display form to collect relevant medical history"""
    st.markdown("### 📋 Medical Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age_group = st.selectbox(
            "Patient Age Group",
            ["Infant", "Child", "Adolescent", "Adult", "Elder", "Unknown"],
            key="medical_age"
        )
    
    with col2:
        allergies = st.text_input(
            "Known Allergies (optional)",
            placeholder="e.g., Penicillin, Nuts",
            key="medical_allergies"
        )
    
    medications = st.text_area(
        "Current Medications (optional)",
        placeholder="e.g., Aspirin, Ibuprofen",
        key="medical_meds",
        height=50
    )
    
    conditions = st.multiselect(
        "Pre-existing Conditions (optional)",
        ["Diabetes", "Heart Disease", "Asthma", "Hypertension", "Arthritis", "Other"],
        key="medical_conditions"
    )
    
    return {
        "age_group": age_group,
        "allergies": allergies,
        "medications": medications,
        "conditions": conditions
    }


def display_specialist_recommendation(injury_type: str, severity: str):
    """
    Display specialist recommendation
    
    Args:
        injury_type: Type of injury
        severity: Severity level
    """
    st.markdown("### 🎯 Recommended Specialist")
    
    specialist_map = {
        "burn": "Dermatologist or Burn Specialist",
        "fracture": "Orthopedic Surgeon",
        "cut": "Surgeon or Primary Care Physician",
        "head injury": "Neurologist",
        "eye injury": "Ophthalmologist",
        "poison": "Toxicologist or Emergency Medicine Specialist",
        "allergic": "Allergist/Immunologist",
        "cardiac": "Cardiologist"
    }
    
    specialist = specialist_map.get(injury_type.lower(), "Primary Care Physician")

    # Build a user-friendly 'find nearby' search link using Google Maps
    def build_find_nearby_link(specialist_name: str, location: str = None) -> str:
        query = f"{specialist_name} near me" if not location else f"{specialist_name} near {location}"
        return f"https://www.google.com/maps/search/{urllib.parse.quote_plus(query)}"
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info(f"👨‍⚕ {specialist}")
    
    with col2:
        st.caption(f"For a {severity} {injury_type}")

        # Provide a direct link to search for the suggested specialist nearby
        try:
            find_url = build_find_nearby_link(specialist)
            st.markdown(f"*Find nearby:* [Search for {specialist}]({find_url})")
        except Exception:
            # Fallback text if building the link fails
            st.write("Find nearby specialists using your preferred map or directory service.")


def display_follow_up_care(injury_type: str):
    """
    Display follow-up care recommendations
    
    Args:
        injury_type: Type of injury
    """
    st.markdown("### 📅 Follow-Up Care")
    
    follow_up_guidance = {
        "minor cut": "Monitor for infection. Return in 7 days for suture removal.",
        "moderate burn": "Apply topical treatment daily. Follow up in 3-5 days.",
        "sprain": "Continue RICE protocol. Follow up in 5-7 days.",
        "fracture": "Immobilize and seek immediate x-ray. Follow up weekly.",
        "allergic reaction": "Avoid allergen. Follow up with allergist in 1-2 weeks.",
    }
    
    guidance = follow_up_guidance.get(injury_type.lower(), 
                                     "Follow doctor's instructions for follow-up care.")
    
    st.info(guidance)