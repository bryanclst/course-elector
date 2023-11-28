from src.models import AppUser, Course, Rating, Post, Comment
from utils import clear_db, populate_db

def test(test_client):
    populate_db()
    assert True