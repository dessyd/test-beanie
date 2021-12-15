from pydantic import BaseSettings

class Settings(BaseSettings):
    database_driver: str = "mongodb"
    database_hostname: str = "mongo"
    database_port: str = "27017"
    database_name: str = "beanie"

    database_username: str
    database_password: str

    class Config:
        env_file = ".env"

settings = Settings()