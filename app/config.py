from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    elasticsearch_url: str = "http://localhost:9200"
    openrouter_api_key: str
    apollo_api_key: str = ""
    hunter_api_key: str = ""
    smtp_host: str = ""
    smtp_user: str = ""
    smtp_password: str = ""
    daily_send_limit: int = 5
    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_project: str | None = None
    candidate_name:str | None = None
    prospeo_api_key: str
    ollama_api_key:str

    class Config:
        env_file = ".env"

settings = Settings()