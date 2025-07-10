import pytest

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/user/", json={
        "name": "Alice",
        "last_name": "Smith",
        "email": "alice@test.com",
        "password": "secure123"
    })
    assert response.status_code == 200
    assert "token" in response.json()

@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    # Primer intento
    await client.post("/user/", json={
        "name": "Bob",
        "last_name": "Brown",
        "email": "bob@test.com",
        "password": "secure456"
    })

    # Segundo intento con el mismo correo
    response = await client.post("/user/", json={
        "name": "Bob",
        "last_name": "Brown",
        "email": "bob@test.com",
        "password": "secure456"
    })
    assert response.status_code == 400 or response.status_code == 409

@pytest.mark.asyncio
async def test_login_user(client):
    await client.post("/user/", json={
        "name": "Carlos",
        "last_name": "Garcia",
        "email": "carlos@test.com",
        "password": "mypass123"
    })
    response = await client.post("/user/login", json={
        "username": "carlos@test.com",
        "password": "mypass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = await client.post("/user/login", json={
        "username": "wronguser@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_list_all_users(client):
    await client.post("/user/", json={
        "name": "Daniela",
        "last_name": "Martinez",
        "email": "daniela@test.com",
        "password": "secure999"
    })
    response = await client.get("/user/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
