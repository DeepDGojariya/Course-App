from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest, asyncio
from main import app

client = TestClient(app)
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['courses']


def test_get_courses_sort_by_alphabetical():
    """Test for get courses sort by alphabetical"""
    response = client.get("/courses?sort_by=alphabetical")
    assert response.status_code == 200
    

def test_get_courses_sort_by_date():
    response = client.get("/courses?sort_by=date")
    assert response.status_code == 200


def test_get_courses_sort_by_rating():
    response = client.get("/courses?sort_by=rating")
    assert response.status_code == 200


def test_get_courses_filter_by_domain():
    response = client.get("/courses?domain=mathematics")
    assert response.status_code == 200


def test_get_course_by_id_exists():
    response = client.get("/courses/3261")
    assert response.status_code == 200
     
     
def test_get_course_by_id_not_exists():
    response = client.get("/courses/xyz")
    assert response.status_code == 404


def test_get_chapter_info():
    response = client.get("/courses/3261/chapters/1")
    assert response.status_code == 200
    
    
def test_get_chapter_info_not_exists():
    response = client.get("/courses/3261/chapters/999")
    assert response.status_code == 404


def test_rate_course_chapter():
    course_id = "3261"
    chapter_id = "1"
    rating = "positive"

    response = client.post(f"/courses/{course_id}/{chapter_id}", data={"rating": rating})
    assert response.status_code == 200

