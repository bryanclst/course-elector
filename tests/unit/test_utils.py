from src.models import AppUser, Course, Rating, Post, Comment, db
from utils import clear_db, populate_db, heavily_populate_db, users_db

def test_users_db(test_client):
    users_db()

    user1 = AppUser.query.filter_by(username='user1').first()
    user2 = AppUser.query.filter_by(username='user2').first()

    assert user1 is not None
    assert user1.email == 'user1@example.com'
    assert user1.hashed_password == 'hashed_password_1'

    assert user2 is not None
    assert user2.email == 'user2@example.com'
    assert user2.hashed_password == 'hashed_password_2'

    all_users = AppUser.query.all()
    assert len(all_users) == 2




