"""App settings."""

from environs import Env
from pydantic import BaseSettings

env = Env()


class Settings(BaseSettings):
    """Basic settings for the application."""

    TITLE: str = "Oak Signs"
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "Management app for notifications around Minecraft APIs"
    DEBUG: bool = env.bool("DEBUG", default=False)


settings = Settings()
