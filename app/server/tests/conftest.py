import pytest
from httpx import AsyncClient
from pymongo import MongoClient
from httpx import AsyncClient, ASGITransport


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.app import app


TEST_DB_URI = "mongodb+srv://rootuser:rootpassword@cluster0.zv4drbw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

@pytest.fixture(scope="module")
async def test_app():
    client = AsyncClient(app=app, base_url="http://test")
    yield client
    await client.aclose()

@pytest.fixture(scope="module")
async def test_db():
    client = MongoClient(TEST_DB_URI)
    db = client.get_default_database()
    yield db
    client.drop_database("test_db")  # clean up