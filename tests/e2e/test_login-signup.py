from utils import heavily_populate_db, populate_db, clear_db
from app import repository_singleton
from src.models import AppUser

def test_client():
    clear_db()
    populate_db()

def test_signup(test_client):
    response = test_client.post('/process_form', data={'username':'new_user', 'hashed_password':'password', 'action':'Sign Up'})
    assert response.status_code == 200
    assert b'Account created sucessfully' in response.data

def test_signup_existing(test_client):
    response = test_client.post('/process_form', data={'username': 'user1', 'hashed_password': 'password', 'action': 'Sign Up'})
    assert response.status_code == 200
    assert b'Username already exists' in response.data

def test_login(test_client):
    response = test_client.post('/process_form', data={'username': 'user1', 'hashed_password': 'password', 'action': 'Login'})
    assert response.status_code == 302
    assert b'Welcome, user1' in response.data
    
def test_login_incorrect(test_client):
    response = test_client.post('/process_form', data={'username': 'no_user', 'hashed_password': 'wrong_password', 'action': 'Login'})
    assert response.status_code == 200
    assert b'Incorrect username or password' in response.data