import pytest
from utils import clear_db, populate_db ,heavily_populate_db
from app import repository_singleton
from src.models import AppUser
from app import app, db

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

    # Combine messages from different categories
    all_messages = message_strings
    print(f"All messages: {all_messages}")

    # Assert that the expected message is present in the combined messages
    assert 'Username already exists' in all_messages


def test_login():
    clear_db()

    with app.test_request_context('/process_form', method='POST', data={'username': 'user1', 'hashed_password': 'password', 'action': 'Login'}):
        response = app.full_dispatch_request()

    # Check the response status code
    assert response.status_code == 302

    # Check if the user is redirected to the expected path
    assert '/login_signup' in response.location  # Check the redirected URL
    
def test_login_incorrect(test_client):
    clear_db()
    response = test_client.post('/process_form', data={'username': 'no_user', 'hashed_password': 'wrong_password', 'action': 'Login'})
    assert response.status_code == 302  # Expecting a redirect

    # Check the redirect location (adjust the URL based on your application)
    assert response.headers['Location'].endswith('/login_signup')  
