import os
import pytest
import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from main import app

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def test_db():
    mongo_uri = os.getenv("TEST_MONGO_URI", "mongodb://mongo:27017")
    client = AsyncIOMotorClient(mongo_uri)
    db = client["test_db"]
    yield db
    client.close()  # Limpieza al final del test

@pytest_asyncio.fixture(autouse=True)
async def clear_users_collection(test_db):
    await test_db["users"].delete_many({})