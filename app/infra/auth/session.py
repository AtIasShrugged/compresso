"""Session-based authentication."""
from datetime import datetime, timedelta
from typing import Optional
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from loguru import logger
from ...config import settings


class SessionManager:
    """Manages user sessions with signed cookies."""
    
    def __init__(self):
        self.serializer = URLSafeTimedSerializer(settings.app_secret)
        self.session_max_age = settings.session_max_age
    
    def create_session(self, username: str) -> str:
        """Create signed session token.
        
        Args:
            username: Username to encode in session
            
        Returns:
            Signed session token
        """
        payload = {
            "username": username,
            "created_at": datetime.utcnow().isoformat()
        }
        return self.serializer.dumps(payload)
    
    def validate_session(self, token: str) -> Optional[str]:
        """Validate session token and return username.
        
        Args:
            token: Signed session token
            
        Returns:
            Username if valid, None otherwise
        """
        try:
            payload = self.serializer.loads(token, max_age=self.session_max_age)
            return payload.get("username")
        except SignatureExpired:
            logger.debug("Session expired")
            return None
        except BadSignature:
            logger.warning("Invalid session signature")
            return None
        except Exception as e:
            logger.error(f"Session validation error: {e}")
            return None
    
    def verify_credentials(self, username: str, password: str) -> bool:
        """Verify username and password against config.
        
        Args:
            username: Username to verify
            password: Password to verify
            
        Returns:
            True if credentials are valid
        """
        return (
            username == settings.app_login_user and
            password == settings.app_login_password
        )


# Global session manager instance
session_manager = SessionManager()
