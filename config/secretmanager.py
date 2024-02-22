from dotenv import load_dotenv
from services.logger import get_logger
logger = get_logger()

async def load_data_into_env() -> None:
    """Loads environment variables according """

    load_dotenv(f"env/development/.env")
    logger.info("Loaded secrets into env.")
