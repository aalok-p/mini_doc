import pytest

@pytest.mark.asyncio
async def test_signup(client):
    response = await client.post("/auth/signup", json={
        "email": "alok@example.com",
        "password": "secret123",
        "full_name": "Alok",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alok@example.com"
    assert data["full_name"] == "Alok"
    assert "id" in data

@pytest.mark.asyncio
async def test_signup_duplicate_email(client):
    await client.post("/auth/signup", json={
        "email": "alokdup@example.com",
        "password": "secret123",
        "full_name": "Alok First",
    })
    response = await client.post("/auth/signup", json={
        "email": "alokdup@example.com",
        "password": "secret123",
        "full_name": "Alok Second",
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login(client):
    await client.post("/auth/signup", json={
        "email": "aloklogin@example.com",
        "password": "secret123",
        "full_name": "Alok Pal",
    })
    response = await client.post("/auth/login", data={
        "username": "aloklogin@example.com",
        "password": "secret123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = await client.post("/auth/login", data={
        "username": "alokbad@example.com",
        "password": "wrong",
    })
    assert response.status_code == 400
    assert "Incorrect" in response.json()["detail"]

@pytest.mark.asyncio
async def test_me(client):
    await client.post("/auth/signup", json={
        "email": "alokme@example.com",
        "password": "secret123",
        "full_name": "Alok Kumar",
    })
    login = await client.post("/auth/login", data={
        "username": "alokme@example.com",
        "password": "secret123",
    })
    token = login.json()["access_token"]

    response = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alokme@example.com"
    assert data["full_name"] == "Alok Kumar"

@pytest.mark.asyncio
async def test_me_unauthorized(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401
