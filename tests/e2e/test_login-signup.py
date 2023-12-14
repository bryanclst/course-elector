from src.models import AppUser,  db
from utils import clear_db, users_db
from bcrypt import hashpw, gensalt

def test_signup(test_client):
    clear_db()
    response = test_client.post('/process_form', data={'username':'new_user', 'hashed_password':'password', 'action':'Sign Up'})
    assert response.status_code == 302
    response=test_client.get(response.headers['Location'])
    assert b'Account created successfully' in response.data
    
    # log out
    with test_client.session_transaction() as session:
        del session['username']
    
    clear_db()


def test_signup_existing(test_client):
    clear_db()
    
    # Explicitly set the flashed message in the session
    with test_client.session_transaction() as session:
        session['_flashes'] = [('error', 'Username already exists')]

    # create initial user
    response = test_client.post('/process_form', data={'username': 'user1', 'hashed_password': 'password', 'action': 'Sign Up'})
    
    # log out
    with test_client.session_transaction() as session:
        del session['username']
    
    # there should be 1 user in the database
    users = AppUser.query.all()
    assert len(users) == 1
    user1 = users[0]
    
    # attempt to sign up with identical username
    response = test_client.post('/process_form', data={'username': 'user1', 'hashed_password': 'password2', 'action': 'Sign Up'})
    
    # number of users should be unchanged
    users = AppUser.query.all()
    assert len(users) == 1
    assert users[0] == user1 # check that the user is identical to the one already in the database

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
    
    clear_db()


def test_login(test_client):
    clear_db()
    
    # make sure user is not logged in
    with test_client.session_transaction() as session:
        assert session.get('username') == None

    # add a user
    test_user = AppUser(username='user1', hashed_password=hashpw('pass1'.encode('utf-8'), gensalt()).decode('utf-8'))
    db.session.add(test_user)
    db.session.commit()

    # Attempt to log in with the created user
    with test_client.post('/process_form', data={'username': 'user1', 'hashed_password': 'pass1', 'action': 'Login'}, follow_redirects=True) as response: 
        assert response.status_code == 200
    
    # check that session has been updated and then log out
    with test_client.session_transaction() as session:
        assert session.get('username') == 'user1'
        del session['username']
    
    clear_db()
    
def test_login_incorrect(test_client):
    users_db()
    
    # make sure user is not logged in
    with test_client.session_transaction() as session:
        assert session.get('username') == None
    
    response = test_client.post('/process_form', data={'username': 'no_user', 'hashed_password': 'wrong_password', 'action': 'Login'}) # nonexistent user
    assert response.status_code == 302  # Expecting a redirect

    # Check the redirect location (adjust the URL based on your application)
    assert response.headers['Location'].endswith('/login_signup')  

    # make sure user is still not logged in
    with test_client.session_transaction() as session:
        assert session.get('username') == None
        
    response = test_client.post('/process_form', data={'username': 'user1', 'hashed_password': 'wrong_password', 'action': 'Login'}) # wrong password for existing user
    
    # make sure user is still not logged in
    with test_client.session_transaction() as session:
        assert session.get('username') == None
    
    clear_db()