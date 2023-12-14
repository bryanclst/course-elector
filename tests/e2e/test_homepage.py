from utils import heavily_populate_db, populate_db,clear_db
from app import repository_singleton
from src.models import AppUser,Course,Rating,Post,Comment

def test_homepage(test_client):
    response=test_client.get('/')
    assert response.status_code == 200