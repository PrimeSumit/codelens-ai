from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL:str
    NVIDIA_API_KEY:str
    EMBEDDING_MODEL:str
    model_config=SettingsConfigDict(env_file=".env")
settings=Settings()