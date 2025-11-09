import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


async def check():
    load_dotenv()
    uri = os.getenv("MONGODB_URI")
    if not uri:
        print("MONGODB_URI not set in environment (.env)")
        return
    print(f"Testing MongoDB connection to: {uri}")
    try:
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        info = await client.server_info()
        print("Connected to MongoDB. Server info:")
        print(info)
    except Exception as e:
        print("Failed to connect to MongoDB:", repr(e))


if __name__ == '__main__':
    asyncio.run(check())
