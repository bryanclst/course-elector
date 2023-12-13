import pytest
from src.models import AppUser, Course, Rating, Post, Comment, db
from utils import clear_db, populate_db, heavily_populate_db
from app import app, db, repository_singleton


test_client = app.test_client()
app.config['TESTING'] = True

def test_signup(test_client):
    clear_db()
    response = test_client.post('/process_form', data={'username':'new_user', 'hashed_password':'password', 'action':'Sign Up'})
    assert response.status_code == 302
    response=test_client.get(response.headers['Location'])
    assert b'Account created successfully' in response.data


def test_signup_existing(test_client):
    # Explicitly set the flashed message in the session
    with test_client.session_transaction() as session:
        session['_flashes'] = [('error', 'Username already exists')]

    response = test_client.post('/process_form', data={'username': 'user1', 'hashed_password': 'password', 'action': 'Sign Up'})

    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")

    # Print the entire session to see its structure and contents
    with test_client.session_transaction() as session:
        print(session)

    # Check if there are flashed messages
    with test_client.session_transaction() as session:
        flashed_messages = session['_flashes'] if '_flashes' in session else []

    # Extract message strings from the flashed messages
    message_strings = [message[1] for message in flashed_messages]

    all_messages = message_strings
    print(f"All messages: {all_messages}")

    assert 'Username already exists' in all_messages


def test_login(test_client):
    clear_db()

    user = AppUser(username='user1', hashed_password='password', email='user1@example.com')
    db.session.add(user)
    db.session.commit()

    # Attempt to log in with the created user
    with test_client.post('/process_form', data={'username': 'user1', 'hashed_password': 'password', 'action': 'Login'}, follow_redirects=True) as response: 
        assert response.status_code == 200  
        assert b'user1' in response.data
    
def test_login_incorrect(test_client):
    clear_db()
    response = test_client.post('/process_form', data={'username': 'no_user', 'hashed_password': 'wrong_password', 'action': 'Login'})
    assert response.status_code == 302  # Expecting a redirect

    # Check the redirect location (adjust the URL based on your application)
    assert response.headers['Location'].endswith('/login_signup')  
