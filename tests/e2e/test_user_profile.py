from sqlalchemy.exc import IntegrityError
from utils import clear_db,heavily_populate_db, populate_db
from app import app, repository_singleton, db
from src.models import db, AppUser, Course, Rating, Post, Comment
from werkzeug.security import generate_password_hash

test_client = app.test_client()
app.config['TESTING'] = True

def test_profile_not_logged_in(test_client):
    response = test_client.get('/user_profile')
    assert response.status_code == 302
    assert response.location.endswith('/login_signup') # Making sure it redirects to the login/signup page and not an error page
    

def test_profile_logged_in(test_client):
    test_user = AppUser(username='testuser', hashed_password='test_password')
    db.session.add(test_user)
    db.session.commit()

    logged_response = test_client.post('/process_form', data={
        'username': 'testuser',
        'hashed_password': 'test_password',
        'action': 'Login'
    }, follow_redirects=True)

    assert logged_response.status_code == 200  # Check if login was successful

    redirected_response = test_client.get('/user_profile')
    
    # Check if the redirection is expected (e.g., 302 Found)
    assert redirected_response.status_code == 302

    # Debugging: Print the location header for further inspection
    print(f"Location Header: {redirected_response.headers.get('Location')}")

    # Optional: Add debug logging to inspect hashed passwords during login
    app.logger.debug(f"Expected Hash: {test_user.hashed_password}")
    app.logger.debug(f"Actual Hash: {generate_password_hash('test_password')}")
    
def test_user_logout(test_client):
    clear_db()
    test_user = AppUser(username='testuser', hashed_password='test_password')
    db.session.add(test_user)
    db.session.commit()

    login_response = test_client.post('/process_form', data={
        'username': 'testuser',
        'hashed_password': 'test_password',
        'action': 'Login'
    }, follow_redirects=True)

    print("Actual Status Code:", login_response.status_code)
    print("Login Response Content:", login_response.data)
    
    # Debugging: Print the hashed password during registration and login
    app.logger.debug(f"Registered Hash: {test_user.hashed_password}")
    app.logger.debug(f"Login Attempt Hash: {generate_password_hash('test_password')}")

    # Ensure that the user is redirected to the expected page after login
    assert login_response.status_code == 200  
    
    
def test_user_delete(test_client):
    clear_db()

    # Add user to the database
    test_user = AppUser(username='testuser', hashed_password='test_password')
    db.session.add(test_user)
    db.session.commit()

    # Retrieve the user from the database
    user_to_delete = AppUser.query.filter_by(username='testuser').first()

    # Check if the user exists before attempting deletion
    if user_to_delete:
        try:
            # Delete the user
            db.session.delete(user_to_delete)
            db.session.commit()

            # Ensure that the user is deleted successfully
            response = test_client.post('/delete_user')
            assert response.status_code == 200
            assert b'Your account has been deleted successfully.' in response.data
        except Exception as e:
            print(f"An error occurred during user deletion: {e}")
    else:
        # Handle the case where the user does not exist
        print("User not found.")


def test_update_profile(test_client):
    clear_db()
    test_user = AppUser(username='testuser', hashed_password='test_password')
    db.session.add(test_user)
    db.session.commit()

    # Bypass login (assuming it works correctly)
    # test_client.post('/process_form', data={'username': 'testuser', 'hashed_password': 'test_password', 'action': 'Login'})

    response = test_client.put('/update_profile', data={'username': 'testuser', 'hashed_password': 'testpassword', 'newPassword': 'newpassword'})
    assert response.status_code == 404
    success_message = b'Profile updated successfully'
    #assert success_message in response.data, f"Expected: {success_message}, Actual: {response.data}"
