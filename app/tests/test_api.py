import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_get_rooms():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/rooms")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_booking_unauthorizated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/bookings", json={
            "room_id": 1,
            "start_time": "2026-12-01T10:00:00Z",
            "end_time": "2026-12-01T12:00:00Z",
            "client_contact": "hacker@example.com"
        })

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_full_auth_and_booking_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        unique_email = f"tester_{uuid.uuid4().hex[:6]}@example.com"
        password = "supersecret"

        reg_res = await ac.post("/auth/register", json={
            "email": unique_email,
            "password": password
        })
        assert reg_res.status_code == 201


        login_res = await ac.post("/auth/login", data={
            "username": unique_email,
            "password": password
        })
        assert login_res.status_code == 200


        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        room_res = await ac.post("/rooms", json={
            "name": "Auto-Test Room",
            "capacity": 5,
            "description": "Created by pytest"
        })
        assert room_res.status_code == 200
        room_id = room_res.json()["id"]

        booking_res = await ac.post("/bookings", headers=headers, json={
            "room_id": room_id,
            "start_time": "2027-01-01T15:00:00Z",
            "end_time": "2027-01-01T17:00:00Z",
            "client_contact": unique_email
        })

        assert booking_res.status_code == 200
        assert booking_res.json()["status"] == "active"