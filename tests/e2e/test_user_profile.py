from utils import clear_db,heavily_populate_db, populate_db
from app import repository_singleton, db
from src.models import AppUser
from werkzeug.security import generate_password_hash

def test_profile_not_logged_in(test_client):
    response = test_client.get('/user_profile')
    assert response.status_code == 302
    assert response.location.endswith('/login_signup') #Making sure it redirects to the login/signup page and not an error page
    
def test_profile_logged_in(test_client):
    clear_db()
    #Need to rewrite test case so that it gets information about the user actually logged in. Then they take that to show the credentials for logged in
    #Getting and than displaying
    hashed_password = generate_password_hash('test_password')
    test_user = AppUser(username='testuser', hashed_password=hashed_password)
    db.session.add(test_user)
    db.session.commit()

    response = test_client.post('/pro_form', data={'username': 'testuser', 'hashed_password': 'test_password', 'action': 'Login'}, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Get the response content as text
    result = response.get_data(as_text=True)
    print("Response content:", result)
    
    # Extract a specific section of the response content
    start_marker = '<h2>'
    end_marker = '</h2>'
    
    start_index = result.find(start_marker)
    end_index = result.find(end_marker, start_index)
    
    user_info_section = result[start_index:end_index + len(end_marker)]
    
    # Check if the 'Username: testuser' is present in the extracted section
    assert 'Username: testuser' in user_info_section
# Check for the presence of content on the user profile page
# def test_profile_logged_in(test_client):
#     clear_db()
#     test_user = AppUser(username = 'testuser', hashed_password='test_password')
#     db.session.add(test_user)
#     db.session.commit()
    
#     response = test_client.post('/process_form', data={'username':'testuser', 'hashed_password':'test_password', 'action': 'Login'}, follow_redirects=True)
#     assert response.status_code == 302
#     assert response.location.endswith('/user_profile') #Making sure it goes to the profile page
    
#     response = test_client.get('/user_profile')
#     assert response.status_code == 200
#     assert b'Username: testuser' in response.data
    
def test_update_profile(test_client):
    clear_db()
    test_user = AppUser(username='testuser', hashed_password= 'test_password')
    db.session.add(test_user)
    db.session.commit()
    
    test_client.post('/process_form', data={'username':'testuser', 'hashed_password':'test_password', 'action': 'Login'})
    
    response = test_client.post('/update_profile', data={'username': 'testuser', 'hashed_password': 'testpassword', 'newPassword': 'newpassword'})
    assert response.status_code == 500
    # assert response.location.endswith('/user_profile')
    
    assert b'Profile updated sucessfully' in test_client.get('/user_profile').data
    
    password_update = AppUser.query.filter_by(userrname='testuser').first()
    assert password_update is not None
    assert password_update.check_password('newpassword')
    
def test_user_logout(test_client):
    clear_db()
    test_user = AppUser(username='testuser', hashed_password= 'test_password')
    db.session.add(test_user)
    db.session.commit()
    
    test_client.post('/process_form', data={'username':'testuser', 'hashed_password':'test_password', 'action': 'Login'})
    
    response=test_client.get('/logout')
    assert response.status_code ==302
    assert response.location.endswith('/login_signup')
    
    with test_client.session_transaction() as session:
        assert 'username' not in session
      
    response=test_client.get('/login_signup')
    assert response.status_code == 200  
    assert b'Log In/Sign up' in test_client.get('login_signup').data
    
    
def test_user_delete(test_client):
    clear_db()
    test_user = AppUser(username='testuser', hashed_password= 'test_password')
    db.session.add(test_user)
    db.session.commit()
    
    test_client.post('/process_form', data={'username':'testuser', 'hashed_password':'test_password'})
    response = test_client.post('/delete_user')
    
    assert response.status_code == 500

    