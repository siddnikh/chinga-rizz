from passlib.context import CryptContext

from schema.anthropos import User
from config.db import get_anthropos_db
collection = get_anthropos_db()["users"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#TODO
async def create_user(user: User):
    user.password = hash_password(user.password)
    pass

async def get_user(email: str):
    pass

async def update_user(user_data: User):
    filter = {"email": user_data.email}    
    update_data = {
        "name": user_data.name,
        "age": user_data.age,
        "is_active": user_data.is_active,
    }
    
    try:
        result = collection.update_one(filter, {"$set": update_data})
        if result.matched_count == 1 and result.modified_count == 1 or not user:
            return user_data
        else:
            raise Exception({"status_code": 401, "detail": "User not found or error updating user"})
    except Exception as e:
        raise Exception({"status_code": 500, "detail": "Error updating user: " + str(e)})