from motor.motor_asyncio import AsyncIOMotorClient
import os

def get_db():
    ENV = os.getenv("ENV", "prod")
    if ENV == "test":
        mongo_uri = os.getenv("TEST_MONGO_URI", "mongodb://localhost:27017")
        db_name = "test_db"
    else:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/prod_db")
        db_name = "prod_db"

    client = AsyncIOMotorClient(mongo_uri)
    return client[db_name]
