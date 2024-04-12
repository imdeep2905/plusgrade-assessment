import logging
from logging.handlers import RotatingFileHandler

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Tax Calculator"
    debug: bool = False
    tax_calculator_api_url: str = "http://localhost:5001/tax-calculator/tax-year"
    tax_calculator_retries: int = 3
    tax_calculator_wait_time: int = 1  # in seconds
    tax_calculator_supported_years: list[int] = list(range(2019, 2023))
    logging_file_name: str = "app.log"
    logging_backup_count: int = 10
    logging_max_bytes: int = 1_000_000

    class Config:
        env_file = ".env"


settings = Settings()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(
            settings.logging_file_name,
            maxBytes=settings.logging_max_bytes,
            backupCount=settings.logging_backup_count,
        ),
        logging.StreamHandler(),
    ],
)
