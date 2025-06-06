import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Email Microservice"
    VERSION: str = "1.0.0"
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str
    
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    
    IMAP_HOST: str = "mailhog"  
    IMAP_PORT: int = 143     
    IMAP_USER: str = "test"    
    IMAP_PASSWORD: str = "test"
    
    class Config:
        env_file = ".env"

settings = Settings()