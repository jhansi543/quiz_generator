import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from dotenv import load_dotenv, find_dotenv

# Ensure we load the .env file from the backend folder if present
env_path = find_dotenv(filename=".env", raise_error_if_not_found=False)
if not env_path:
    # try backend relative path
    base_dir = os.path.dirname(__file__)
    candidate = os.path.join(base_dir, ".env")
    if os.path.exists(candidate):
        load_dotenv(candidate)
    else:
        # fallback to default behavior (search upward)
        load_dotenv()
else:
    load_dotenv(env_path)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "project_tracer_db")

client: Optional[AsyncIOMotorClient] = None

def get_database():
    """Return database instance. Motor's connection pooling handles efficiency."""
    # Motor automatically pools connections, so creating "new" clients is efficient
    client = AsyncIOMotorClient(
        MONGODB_URI,
        maxPoolSize=1,  # Limit pool size in serverless
        serverSelectionTimeoutMS=5000,
    )
    return client[DATABASE_NAME]


async def close_database():
    global client
    if client is not None:
        client.close()
        client = None
