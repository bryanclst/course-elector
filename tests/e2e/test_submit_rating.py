from src.models import AppUser, Course, Rating, Post, Comment
from utils import clear_db, populate_db, heavily_populate_db

def test(test_client):
    heavily_populate_db()
    assert True