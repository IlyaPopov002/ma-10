import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    amqp_url: str = os.getenv("AMQP_URL")
    postgres_url_book: str = os.getenv("POSTGRES_URL_BOOK")


settings = Settings()
