from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    WheatherToken: str
    BaseUrl: str
    GeoPrefix: str
    WheatherPrefix: str
    
    model_config = SettingsConfigDict(env_file=".env")
    
    
settings = Settings()