# tests/test_students.py
import pytest
from httpx import AsyncClient, ASGITransport
import sys
import os
from starlette.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.app import app

# CREATE STUDENT

@pytest.mark.asyncio
async def test_create_student():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        #CREATE STUDENT
        response = await ac.post("/student/", json={
            "fullname": "Test Student",
            "email": "test@example.com",
            "course_of_study": "science",
            "year": 5,
            "gpa":"1.5"
        })
        data = response.json()
        STUDENT_ID = data["data"][0]["id"]
        assert response.status_code == 200
        assert response.json()["message"] == "Student added successfully."


        # GET STUDENT BY ID
        response = await ac.get(f"/student/{STUDENT_ID}")
        assert response.status_code == 200
        data = response.json()
        assert data["data"][0]["fullname"] == "Test Student"
        assert data["data"][0]["GPA"] == 1.5


        # GET ALL STUDENTS
        response = await ac.get("/student/")
        assert response.status_code == 200

        # UPDATE STUDENT
        update_payload = {
            "fullname": "Updated Student222",
        }
        response = await ac.put(f"/student/{STUDENT_ID}", json=update_payload)
        assert response.status_code == 200

        # DELETE STUDENT
        response = await ac.delete(f"/student/{STUDENT_ID}")
        assert response.status_code == 200
        
        # Verify deletion: GET should now 404
        response = await ac.get(f"/student/{STUDENT_ID}")
        data = response.json()
        assert response.json()["code"] == 404
    
