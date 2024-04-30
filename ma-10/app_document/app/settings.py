# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     amqp_url: str
#     postgres_url_book: str
#     postgres_url_document: str

#     model_config = SettingsConfigDict(env_file='.env')


# settings = Settings()

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Определяем путь к .env файлу относительно расположения settings.py
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

print(f"Current working directory: {os.getcwd()}")
print(f"Is .env file present: {os.path.isfile(env_path)}")
print(f"env_path: {env_path}")


class Settings(BaseSettings):
    amqp_url: str = os.getenv("AMQP_URL")
    postgres_url_document: str = os.getenv("POSTGRES_URL_DOCUMENT")


settings = Settings()
