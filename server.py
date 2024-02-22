import os
import sys
from pathlib import Path
from fastapi import FastAPI

from hypercorn.config import Config
from hypercorn.asyncio import serve

from config.secretmanager import load_data_into_env
import asyncio


base_dir = Path(__file__).resolve().parent
sys.path.append(str(base_dir))

app = FastAPI()

from services.logger import setup_logging, get_logger

setup_logging()
logger = get_logger()

@app.get("/hello")
def hello():
    return 'world'

async def main():
    await load_data_into_env()
    config = Config()
    port = os.getenv("HTTP_PORT", "5001")
    config.bind = [f"0.0.0.0:{port}"]
    logger.info("HTTP Server running on port " + os.environ.get('HTTP_PORT', "5001"));
    await serve(app, config)


if __name__ == '__main__':

    logger.info("Starting server...")
    logger.info("CURRENT ENVIRONMENT: " + os.environ.get('RUNTIME_ENV'))
    
    asyncio.run(main())