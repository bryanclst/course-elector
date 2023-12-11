from utils import heavily_populate_db, populate_db,clear_db
from app import repository_singleton, db
from src.models import AppUser

def test_profile_not_logged_in(test_client):
    response = test_client.get('/user_profile')
    assert response.status_code == 302
    assert response.location.endswith('/login_signup') #Making sure it redirects to the login/signup page and not an error page
    
def test_profile_logged_in(test_client):
    clear_db()
    test_user = AppUser(username = 'testuser', hashed_password='test_password')
    db.session.add(test_user)
    db.session.commit()
    
    response = test_client.post('/process_form', data={'username':'testuser', 'hashed_password':'test_password', 'action': 'Login'})
    assert response.status_code == 302
    assert response.location.endswith('/user_profile') #Making sure it goes to the profile page
    
    response = test_client.get('/user_profile')
    assert response.status_code == 200
    assert b'Username: testuser' in response.data
    
def test_update_profile(test_client):
    clear_db()
    test_user = AppUser(username='testuser', hashed_password= 'test_password')
    db.session.add(test_user)
    db.session.commit()
    
    test_client.post('/process_form', data={'username':'testuser', 'hashed_password':'test_password', 'action': 'Login'})
    
    response = test_client.post('/update_profile', data={'username': 'testuser', 'hashed_password': 'testpassword', 'newPassword': 'newpassword'})
    assert response.status_code ==302
    assert response.location.endswith('/user_profile')
    
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
        
    assert b'Log In/Sign up' in test_client.get('login_signup').data
    
    
def test_user_delete(test_client):
    clear_db()
    test_user = AppUser(username='testuser', hashed_password= 'test_password')
    db.session.add(test_user)
    db.session.commit()
    
    test_client.post('/process_form', data={'username':'testuser', 'hashed_password':'test_password'})
    response = test_client.post('/delete_user')
    assert response.status_code == 302
    assert b'Redirecting...' in response.data
    assert b'href="/login_signup"' in response.data
    assert response.headers['Location'].endswith('/login_signup')

    
    delete_user = AppUser.query.filter_by(username='testuser').first()
    assert delete_user is None
    
    assert b'Account deleted sucessfully' in test_client.get('/login_signup').data
    
    