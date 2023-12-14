from flask import session
from flask_bcrypt import Bcrypt
import bcrypt
from sqlalchemy.exc import IntegrityError
from utils import clear_db,heavily_populate_db, populate_db
from app import app, repository_singleton, db
from src.models import db, AppUser, Course, Rating, Post, Comment
from werkzeug.security import generate_password_hash, check_password_hash

test_client = app.test_client()
app.config['TESTING'] = True

def test_profile_not_logged_in(test_client):
    # make sure user is not logged in
    with test_client.session_transaction() as session:
        assert not session.get('username')
    
    response = test_client.get('/user_profile')
    assert response.status_code == 302
    assert response.location.endswith('/login_signup') # Making sure it redirects to the login/signup page and not an error page
    

def test_profile_logged_in(test_client):
    clear_db()
    
    test_user = AppUser(username='testuser', hashed_password=bcrypt.hashpw('test_password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
    db.session.add(test_user)
    db.session.commit()

    logged_response = test_client.post('/process_form', data={
        'username': 'testuser',
        'hashed_password': 'test_password',
        'action': 'Login'
    }, follow_redirects=True)

    assert logged_response.status_code == 200  # Check if login was successful
    with test_client.session_transaction() as session:
        assert session.get('username') == 'testuser'

    # redirected_response = test_client.get('/user_profile')
    
    response = test_client.get('/user_profile')
    assert response.status_code == 200 # will be 302 if not logged in
    assert b'<title>User Profile</title>' in logged_response.data
    
    # # Check if the redirection is expected (e.g., 302 Found)
    # assert redirected_response.status_code == 302

    # # Debugging: Print the location header for further inspection
    # print(f"Location Header: {redirected_response.headers.get('Location')}")

    # # Optional: Add debug logging to inspect hashed passwords during login
    # app.logger.debug(f"Expected Hash: {test_user.hashed_password}")
    # app.logger.debug(f"Actual Hash: {generate_password_hash('test_password')}")
    
    # log out
    with test_client.session_transaction() as session:
        del session['username']
    
    clear_db()
    
def test_user_logout(test_client):
    clear_db()
    test_user = AppUser(username='testuser', hashed_password=bcrypt.hashpw('test_password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
    db.session.add(test_user)
    db.session.commit()

    # Perform login
    login_response = test_client.post('/process_form', data={
        'username': 'testuser',
        'hashed_password': 'test_password',
        'action': 'Login'
    }, follow_redirects=True)
    
    assert login_response.status_code == 200
    with test_client.session_transaction() as session:
        assert session.get('username') == 'testuser'
        
    # Perform logout
    logout_response = test_client.get('/logout', follow_redirects=True)

    assert logout_response.status_code == 200
    assert b'You have been logged out' in logout_response.data
    with test_client.session_transaction() as session:
        assert session.get('username') == None

    # Check the redirected URL if it's not None
    if logout_response.location:
        assert any('/login_signup' in url for url in [logout_response.location])
    
    clear_db()

def test_user_delete(test_client):
    clear_db()

    # Add user to the database
    test_user = AppUser(username='testuser', hashed_password='test_password')
    db.session.add(test_user)
    db.session.commit()
    
    users = AppUser.query.all()
    assert len(users) == 1

    # simulate login
    with test_client.session_transaction() as session:
        session['username'] = 'testuser'
    
    response = test_client.post('/delete_user', follow_redirects=True)
    assert response.status_code == 200
    
    users = AppUser.query.all()
    assert not users
    with test_client.session_transaction() as session:
        assert not session.get('username')

    # Retrieve the user from the database
    # user_to_delete = AppUser.query.filter_by(username='testuser').first()

    # # Check if the user exists before attempting deletion
    # if user_to_delete:
    #     try:
    #         # Delete the user
    #         db.session.delete(user_to_delete)
    #         db.session.commit()

    #         # Ensure that the user is deleted successfully
    #         response = test_client.post('/delete_user')
    #         assert response.status_code == 200
    #         assert b'Your account has been deleted successfully.' in response.data
    #     except Exception as e:
    #         print(f"An error occurred during user deletion: {e}")
    # else:
    #     # Handle the case where the user does not exist
    #     print("User not found.")
    
    clear_db()

def test_update_profile(test_client):
    clear_db()
    
    hashed_password = bcrypt.hashpw('test_password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    test_user = AppUser(username='testuser', hashed_password=hashed_password)
    db.session.add(test_user)
    db.session.commit()
    
    # verify that the original password generated is the same as testuser's
    assert hashed_password == AppUser.query.filter_by(username='testuser').first().hashed_password

    # simulate login
    with test_client.session_transaction() as session:
        session['username'] = 'testuser'
    
    with app.test_request_context('/update_profile'):
        # Bypass login if necessary
        # if 'user_id' not in session:
        #     session['user_id'] = test_user.user_id

        # Update the profile
        response = test_client.post(
            '/update_profile/{user_id}'.format(user_id=test_user.user_id),
            data={'hashed_password': 'test_password', 'new_password': 'newpassword'}
        )
    
    assert response.status_code == 302, f"Unexpected status code: {response.status_code}"
    
    # original password no longer equal to testuser's password
    assert hashed_password != AppUser.query.filter_by(username='testuser').first().hashed_password
    
    # log out
    with test_client.session_transaction() as session:
        del session['username']
        
    clear_db()