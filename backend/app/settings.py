from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_secret: str = "grounded-agent-dev-secret"
    database_url: str = "sqlite:///./grounded_agent.db"
    min_grounding_score: float = 0.12
    daily_token_budget: int = 20000
    class Config:
        env_file = ".env"
