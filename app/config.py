import os

from pydantic_settings import BaseSettings

from enums import Environment


class BaseConfig(BaseSettings):
    SECRET_KEY: str = os.getenv('FAST_API_SECRET_KEY', '')
    ALLOWED_HOSTS: list[str] = os.getenv(
        'FAST_API_ALLOWED_HOSTS', ['localhost']).split(',')
    DEBUG: bool = bool(int(os.getenv('DEBUG', 0)))


class DevelopmentConfig(BaseConfig):
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    POSTGRES_URL: str = os.getenv('DEV_POSTGRES_URL', '')

    GEMINI_API_KEY: str = os.getenv('DEV_GEMINI_API_KEY', '')
    GEMINI_MODEL: str = os.getenv('DEV_GEMINI_MODEL', '')
    GEMINI_MAX_OUTPUT_TOKENS: int = \
        os.getenv('DEV_GEMINI_MAX_OUTPUT_TOKENS', 3000)
    GEMINI_TEMPERATURE: float = os.getenv('DEV_GEMINI_TEMPERATURE', 1.0)


class ProductionConfig(BaseConfig):
    ENVIRONMENT: Environment = Environment.PRODUCTION
    POSTGRES_URL: str = os.getenv('PROD_POSTGRES_URL', '')

    GEMINI_API_KEY: str = os.getenv('PROD_GEMINI_API_KEY', '')
    GEMINI_MODEL: str = os.getenv('PROD_GEMINI_MODEL', '')
    GEMINI_MAX_OUTPUT_TOKENS: int = \
        os.getenv('PROD_GEMINI_MAX_OUTPUT_TOKENS', 3000)
    GEMINI_TEMPERATURE: float = os.getenv('PROD_GEMINI_TEMPERATURE', 1.0)


def get_config(env: str):
    """Convert configs class to dict."""
    export_config_list = [
        DevelopmentConfig,
        ProductionConfig,
    ]

    cfg_class_map = {
        cfg().ENVIRONMENT: cfg()
        for cfg in export_config_list
    }

    return cfg_class_map[env]


env = Environment(os.getenv('ENV', Environment.DEVELOPMENT.name))
settings = get_config(env)
