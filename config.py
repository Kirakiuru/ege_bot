import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)


class Settings(BaseSettings):

    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8')


config = Settings()
