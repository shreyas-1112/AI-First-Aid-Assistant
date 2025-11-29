"""
Result cards component for displaying first aid results
"""
import streamlit as st
from typing import Dict, List, Any


def display_injury_analysis_card(analysis: Dict[str, Any]):
    """
    Display injury analysis card
    
    Args:
        analysis: Analysis result dictionary
    """
    st.markdown("### 🔍 Injury Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        injury_type = analysis.get("injury_type", "Unknown")
        st.metric("Injury Type", injury_type)
    
    with col2:
        severity = analysis.get("severity", "Unknown")
        severity_color = {
            "mild": "🟢",
            "moderate": "🟡",
            "severe": "🔴"
        }.get(severity.lower(), "⚪")
        st.metric("Severity", f"{severity_color} {severity}")
    
    with col3:
        affected_area = analysis.get("affected_area", "Unknown")
        st.metric("Affected Area", affected_area)
    
    with col4:
        confidence = analysis.get("confidence_score", 0.0)
        st.metric("Confidence", f"{confidence*100:.1f}%")


def display_first_aid_steps(steps: List[Dict[str, Any]]):
    """
    Display first aid steps
    
    Args:
        steps: List of first aid steps
    """
    st.markdown("### 🚑 First Aid Steps")
    
    for step in steps:
        with st.expander(f"Step {step['order']}: {step['title']}", expanded=False):
            st.markdown(f"**Description:** {step['description']}")
            
            if step.get('warning'):
                st.warning(f"⚠️ **Warning:** {step['warning']}")
            
            if step.get('duration'):
                st.info(f"⏱️ **Duration:** {step['duration']}")


def display_emergency_alert(is_emergency: bool):
    """
    Display emergency alert if needed
    
    Args:
        is_emergency: Whether this is an emergency
    """
    if is_emergency:
        st.error("""
        ### 🚨 THIS IS AN EMERGENCY SITUATION 🚨
        
        **CALL 911 IMMEDIATELY**
        
        Do not delay seeking professional emergency help.
        """)


def display_professional_help(professional_help: str):
    """
    Display professional help information
    
    Args:
        professional_help: Professional help text
    """
    st.markdown("### 👨‍⚕️ When to Seek Professional Help")
    st.info(professional_help)


def display_age_guidance(age_group: str, guidance: Dict[str, Any]):
    """
    Display age-appropriate guidance
    
    Args:
        age_group: Age group of patient
        guidance: Age guidance information
    """
    st.markdown(f"### 👶 Age-Specific Guidance ({age_group})")
    
    if guidance.get("special_considerations"):
        st.markdown("**Special Considerations:**")
        for consideration in guidance["special_considerations"]:
            st.write(f"• {consideration}")
    
    if guidance.get("warnings"):
        st.markdown("**Important Warnings:**")
        for warning in guidance["warnings"]:
            st.warning(warning, icon="⚠️")


def display_prevention_tips(tips: List[str]):
    """
    Display prevention tips
    
    Args:
        tips: List of prevention tips
    """
    st.markdown("### 🛡️ Prevention Tips")
    
    for i, tip in enumerate(tips, 1):
        st.write(f"{i}. {tip}")
