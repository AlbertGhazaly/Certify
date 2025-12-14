from pydantic_settings import BaseSettings  

class Settings(BaseSettings):
    app_name: str = "Certify"
    database_url: str

    class Config:
        extra = "allow"
        env_file = ".env" 

settings = Settings()