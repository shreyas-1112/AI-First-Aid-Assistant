"""
Hospital Locator Component - Display nearby hospitals and medical facilities
"""
import streamlit as st
from config.languages import get_translation
from backend.services.hospital_locator import HospitalLocator


def get_text(key: str) -> str:
    """Get translated text for current language"""
    language = st.session_state.get("language", "en")
    return get_translation(language, key)


def display_hospital_locator():
    """Display hospital locator interface"""
    st.markdown(f"### 🏥 {get_text('find_hospitals')}")
    
    st.write(get_text('enter_location'))
    
    # Form for hospital search
    with st.form("hospital_location_form", clear_on_submit=True):
        address = st.text_input(
            f"{get_text('find_hospitals')}:",
            placeholder="e.g., 123 Main St, City, State or 12345",
            key="hospital_address_input"
        )
        
        radius = st.slider(
            get_text('search_radius'),
            min_value=1,
            max_value=50,
            value=5,
            step=1,
            key="hospital_radius_slider"
        )
        
        submitted = st.form_submit_button("🔍 " + get_text('find_hospitals'), type="primary")
        
        if submitted and address:
            with st.spinner(get_text('finding_hospitals')):
                try:
                    locator = HospitalLocator()
                    
                    # Get coordinates from address
                    coords = locator.get_address_coordinates(address)
                    if coords:
                        lat, lon = coords
                        
                        # Get hospitals near the location
                        hospitals = locator.get_hospitals_near_location(lat, lon, radius_km=radius)
                        
                        if hospitals:
                            st.session_state.hospitals_found = hospitals
                            display_hospitals(hospitals)
                            
                            # Show map
                            st.markdown("---")
                            st.markdown(f"### {get_text('hospital_map')}")
                            display_hospital_map(hospitals)
                        else:
                            st.warning(get_text('no_hospitals_found'))
                    else:
                        st.error(f"Could not find coordinates for address: {address}")
                        
                except Exception as e:
                    st.error(f"Error finding hospitals: {str(e)}")


def display_hospitals(hospitals: list):
    """Display found hospitals in a formatted way"""
    if not hospitals:
        st.warning(get_text('no_hospitals_found'))
        return
    
    st.markdown(f"### 🏥 {get_text('nearby_facilities')}")
    st.markdown(f"✅ {get_text('hospitals_found')} **{len(hospitals)}** {get_text('facilities')}:")
    
    for idx, hospital in enumerate(hospitals, 1):
        with st.expander(
            f"**{idx}. {hospital.get('name', get_text('unknown'))}** - {hospital.get('distance_km', 'N/A')} {get_text('km_away')}",
            expanded=(idx == 1)
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Basic info
                if hospital.get('type'):
                    st.markdown(f"**{get_text('hospital_type')}:** {hospital.get('type')}")
                st.markdown(f"**{get_text('hospital_distance')}:** {hospital.get('distance_km', 'N/A')} km")
                
                # Contact info
                if hospital.get('phone'):
                    st.markdown(f"**{get_text('hospital_phone')}** {hospital.get('phone')}")
                
                # Operating hours
                if hospital.get('opening_hours'):
                    st.markdown(f"**{get_text('hospital_hours')}** {hospital.get('opening_hours')}")
                
                # Operator/Organization
                if hospital.get('operator'):
                    st.markdown(f"**{get_text('hospital_organization')}:** {hospital.get('operator')}")
                
                # Website
                if hospital.get('website'):
                    st.markdown(f"**{get_text('hospital_website')}** [{hospital.get('website')}]({hospital.get('website')})")
            
            with col2:
                col_map, col_nav = st.columns(2)
                
                with col_map:
                    if st.button(
                        get_text('hospital_map'),
                        key=f"map_{idx}",
                        use_container_width=True,
                        help="View on Google Maps"
                    ):
                        st.write(f"[Open in Google Maps]({hospital.get('google_maps_url')})")
                
                with col_nav:
                    if st.button(
                        get_text('hospital_navigate'),
                        key=f"nav_{idx}",
                        use_container_width=True,
                        help="Navigate to this location"
                    ):
                        st.write(f"[Open Navigation]({hospital.get('osm_url', hospital.get('google_maps_url'))})")
            
            # Additional info
            st.markdown("---")
            if hospital.get('latitude') and hospital.get('longitude'):
                st.caption(f"{get_text('hospital_coordinates')}: {hospital.get('latitude')}, {hospital.get('longitude')}")


def display_hospital_map(hospitals: list):
    """Display hospitals on a map using Streamlit's native map feature"""
    if not hospitals or len(hospitals) == 0:
        return
    
    # Prepare data for map
    map_data = []
    for hospital in hospitals:
        if hospital.get("latitude") and hospital.get("longitude"):
            map_data.append({
                "latitude": float(hospital.get("latitude")),
                "longitude": float(hospital.get("longitude")),
            })
    
    if map_data:
        # Create map
        st.map(
            map_data,
            zoom=12,
            use_container_width=True
        )
        st.caption("🔴 Red pins show hospital locations")
    else:
        st.warning("Could not display map - no valid coordinates")

