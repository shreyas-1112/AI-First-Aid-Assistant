"""
API client for frontend communication with backend
"""
import requests
from typing import Dict, Any, Optional
import os
from config.settings import BACKEND_URL


class APIClient:
    """Client for communicating with the backend API"""
    
    def __init__(self, base_url: str = BACKEND_URL):
        """
        Initialize API client
        
        Args:
            base_url: Base URL of the backend API
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def upload_image(self, image_path: str, age_group: str = None) -> Dict[str, Any]:
        """
        Upload and analyze an image
        
        Args:
            image_path: Path to image file
            age_group: Optional age group
        
        Returns:
            Analysis result
        """
        try:
            with open(image_path, 'rb') as f:
                files = {'file': f}
                params = {}
                if age_group:
                    params['age_group'] = age_group
                
                response = self.session.post(
                    f"{self.base_url}/analyze/image",
                    files=files,
                    params=params,
                    timeout=30
                )
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.ConnectionError:
            return {"error": "Could not connect to backend. Is it running?"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_first_aid_guidance(
        self,
        injury_type: str,
        severity: str,
        affected_area: str = None,
        age_group: str = "adult"
    ) -> Dict[str, Any]:
        """
        Get first aid guidance for an injury
        
        Args:
            injury_type: Type of injury
            severity: Severity level
            affected_area: Affected area
            age_group: Patient age group
        
        Returns:
            First aid guidance
        """
        try:
            params = {
                "injury_type": injury_type,
                "severity": severity,
                "age_group": age_group
            }
            if affected_area:
                params["affected_area"] = affected_area
            
            response = self.session.post(
                f"{self.base_url}/first-aid/generate",
                params=params,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            return {"status": "error", "error": {"message": "Request timeout - backend is slow to respond"}}
        except requests.exceptions.ConnectionError:
            return {"status": "error", "error": {"message": "Could not connect to backend. Is it running on port 8000?"}}
        except requests.exceptions.HTTPError as e:
            return {"status": "error", "error": {"message": f"HTTP Error: {e.response.status_code} - {e.response.text[:200]}"}}
        except Exception as e:
            print(f"[DEBUG] First aid guidance error: {type(e).__name__}: {str(e)}")
            return {"status": "error", "error": {"message": str(e)}}
    
    def get_emergency_guidance(self, injury_type: str) -> Dict[str, Any]:
        """
        Get emergency guidance
        
        Args:
            injury_type: Type of injury
        
        Returns:
            Emergency guidance
        """
        try:
            response = self.session.get(
                f"{self.base_url}/first-aid/emergency/{injury_type}",
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return {"error": str(e)}
    
    def get_prevention_tips(self, injury_type: str) -> Dict[str, Any]:
        """
        Get prevention tips
        
        Args:
            injury_type: Type of injury
        
        Returns:
            Prevention tips
        """
        try:
            response = self.session.get(
                f"{self.base_url}/first-aid/prevention/{injury_type}",
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return {"error": str(e)}
    
    
    def transcribe_voice_input(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe voice input from audio file
        
        Args:
            audio_file_path: Path to audio file
        
        Returns:
            Transcription result
        """
        try:
            with open(audio_file_path, 'rb') as f:
                files = {'file': f}
                response = self.session.post(
                    f"{self.base_url}/voice-input/transcribe",
                    files=files,
                    timeout=30
                )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return {"error": str(e)}
    
    def parse_injury_from_voice(self, transcription: str) -> Dict[str, Any]:
        """
        Parse injury information from voice transcription
        
        Args:
            transcription: Voice transcribed text
        
        Returns:
            Parsed injury information
        """
        try:
            params = {"transcription": transcription}
            response = self.session.post(
                f"{self.base_url}/voice-input/parse-injury",
                params=params,
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return {"error": str(e)}
    
    def detect_injury_type_from_voice(self, voice_text: str) -> Dict[str, Any]:
        """
        Detect injury type from voice text
        
        Args:
            voice_text: Voice transcribed text
        
        Returns:
            Detected injury type
        """
        try:
            params = {"voice_text": voice_text}
            response = self.session.post(
                f"{self.base_url}/voice-input/detect-injury-type",
                params=params,
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return {"error": str(e)}
    
    def detect_severity_from_voice(self, voice_text: str) -> Dict[str, Any]:
        """
        Detect severity from voice text
        
        Args:
            voice_text: Voice transcribed text
        
        Returns:
            Detected severity
        """
        try:
            params = {"voice_text": voice_text}
            response = self.session.post(
                f"{self.base_url}/voice-input/detect-severity",
                params=params,
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return {"error": str(e)}
    
    def detect_emergency_from_voice(self, voice_text: str) -> Dict[str, Any]:
        """
        Detect emergency from voice text
        
        Args:
            voice_text: Voice transcribed text
        
        Returns:
            Emergency detection result
        """
        try:
            params = {"voice_text": voice_text}
            response = self.session.post(
                f"{self.base_url}/voice-input/detect-emergency",
                params=params,
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return {"error": str(e)}
    
    def get_voice_input_status(self) -> Dict[str, Any]:
        """
        Get voice input service status
        
        Returns:
            Voice input status
        """
        try:
            response = self.session.get(
                f"{self.base_url}/voice-input/status",
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return {"error": str(e)}
    
    def health_check(self) -> bool:
        """
        Check if backend is available
        
        Returns:
            True if backend is healthy
        """
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def close(self):
        """Close the session"""
        self.session.close()
