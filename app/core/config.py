from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    database_url: str
    telegram_bot_token: str
    redis_url: str

    class Config:
        env_file = ".env"


settings = Settings()
