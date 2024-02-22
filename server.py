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

# User Routes
@app.post("/signup", response_model=User)
async def signup(user: User):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    await create_user(user)
    return user

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # ... (generate access token)

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user_info(user_id: int, user_data: User):
    user = await get_user(user_data.email)  # Use email for consistency
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Update allowed fields (exclude password)
    user.name = user_data.name
    user.age = user_data.age
    await update_user(user)
    return user

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