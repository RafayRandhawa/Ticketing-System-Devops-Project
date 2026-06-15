"""
Configuration module for FastAPI application
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Database (Supabase)
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_role_key: Optional[str] = None
    database_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    host: str
    port: int

    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    email_address: Optional[str] = None
    email_password: Optional[str] = None
    
    # JWT
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # QR Code
    qr_code_size: int = 10
    qr_code_border: int = 4
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
