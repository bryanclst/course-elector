import pytest
from utils import clear_db, populate_db ,heavily_populate_db
from app import repository_singleton
from src.models import AppUser

def test_signup(test_client):
    clear_db()
    response = test_client.post('/process_form', data={'username':'new_user', 'hashed_password':'password', 'action':'Sign Up'})
    assert response.status_code == 302
    response=test_client.get(response.headers['Location'])
    assert b'Account created successfully' in response.data

def test_signup_existing(test_client):
    response = test_client.post('/process_form', data={'username': 'user1', 'hashed_password': 'password', 'action': 'Sign Up'})
    assert response.status_code == 302
    response=test_client.get(response.headers['Location'])
    response_data=response.data.decode('utf-8')
    print(response_data)
    assert 'Username already exists' in response_data


def test_login(test_client):
    clear_db()
    response = test_client.post('/process_form', data={'username': 'user1', 'hashed_password': 'password', 'action': 'Login'})
    assert response.status_code == 302
    assert b'Welcome, user1' in response.data
    
def test_login_incorrect(test_client):
    clear_db()
    response = test_client.post('/process_form', data={'username': 'no_user', 'hashed_password': 'wrong_password', 'action': 'Login'})
    assert response.status_code == 200
    assert b'Incorrect username or password' in response.data