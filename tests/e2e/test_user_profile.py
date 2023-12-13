from sqlalchemy.exc import IntegrityError
from utils import clear_db,heavily_populate_db, populate_db
from app import app, repository_singleton, db
from src.models import db, AppUser, Course, Rating, Post, Comment
from werkzeug.security import generate_password_hash

test_client = app.test_client()
app.config['TESTING'] = True

def clear_db():
    try:
        db.session.query(Comment).delete()
        db.session.query(AppUser).delete()
        db.session.query(Course).delete()
        db.session.query(Rating).delete()
        db.session.query(Post).delete()
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

def test_profile_not_logged_in(test_client):
    response = test_client.get('/user_profile')
    assert response.status_code == 302
    assert response.location.endswith('/login_signup') # Making sure it redirects to the login/signup page and not an error page
    
# def test_profile_logged_in(test_client):
#     clear_db()
#     #Need to rewrite test case so that it gets information about the user actually logged in. Then they take that to show the credentials for logged in
#     #Getting and than displaying
#     hashed_password = generate_password_hash('test_password')
#     test_user = AppUser(username='testuser', hashed_password=hashed_password)
#     db.session.add(test_user)
#     db.session.commit()

#     logged_response = test_client.post('/process_form', data={'username': 'testuser', 'hashed_password': 'test_password', 'action': 'Login'}, follow_redirects=True)
    
#     assert logged_response.status_code == 200
#     get_user= test_client.get('/user_profile')
#     assert get_user.status_code == 302
#     # assert get_user.location.endswith('/user_profile')
#     # Get the response content as text
#     result = logged_response.location
#     # get_user.get_data
#     print("Response content:", result)
    
#     # Extract a specific section of the response content
#     # start_marker = '<h2>'
#     # end_marker = '</h2>'
#     # start_index = result.find(start_marker)
#     # end_index = result.find(end_marker, start_index)
#     # user_info_section = result[start_index:end_index + len(end_marker)]
#     # Check if the 'Username: testuser' is present in the extracted section
#     assert 'Username: testuser' in result
# Check for the presence of content on the user profile page
def test_profile_logged_in(test_client):
    test_user = AppUser(username='testuser', hashed_password= 'test_password')
    db.session.add(test_user)
    db.session.commit()
    
    logged_response = test_client.post('/process_form', data={'username': 'testuser', 'hashed_password': 'test_password', 'action': 'Login'}, follow_redirects=True)
    assert logged_response.status_code == 200
        
    # get_user = test_client.get('/user_profile', follow_redirects=True)
    # assert get_user.status_code == 200
    
    
        # Access the redirected page after login
    redirected_response = test_client.get('/user_profile')
    assert redirected_response.status_code == 302  # Assuming the redirected page is accessible
    
    assert 'Some specific content' in logged_response.location
    
    # start_marker = b'<h2>'  # Use 'b' prefix to indicate bytes literals
    # end_marker = b'</h2>'   # Use 'b' prefix to indicate bytes literals
    # result = redirected_response.data  # `result` is in bytes format
    # start_index = result.find(start_marker)
    # end_index = result.find(end_marker, start_index)
    # user_info_section = result[start_index:end_index + len(end_marker)]
    
    
    # # Convert bytes to string for manipulation
    # user_info_section_str = user_info_section.decode('utf-8')  # Decode bytes to string
    
    # # Check if the 'Username: testuser' is present in the extracted section
    # assert 'Username: testuser' in user_info_section.decode('utf-8')# assert b'Welcome, testuser' in get_user.data
        
#      = AppUser(username = 'testuser', hashed_password='test_password')
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
    assert response.status_code == 200
    # assert response.location.endswith('/user_profile')
    
    assert b'Profile updated successfully' in response.data
    
    password_update = AppUser.query.filter_by(userrname='testuser').first()
    assert password_update is not None
    assert password_update.check_password('newpassword')
    
def test_user_logout(test_client):
    test_user = AppUser(username='testuser', hashed_password= 'test_password')
    db.session.add(test_user)
    db.session.commit()
    
    login_response  = test_client.post('/process_form', data={'username':'testuser', 'hashed_password':'test_password', 'action': 'Login'})
    assert login_response.status_code ==302
    
    index_response = test_client('/')
    assert index_response.status_code == 200  
    
    assert b'Logout' in index_response.data
    
    logout = test_client.get('/logout')
    assert logout.status_code ==302
    
    logout_index = test_client.get('/')
    assert logout_index.status_code ==200 
    
    assert b'Log In/Sign up' in index_response.data

    # Check that "Logout" is not present after logging out
    assert b'Logout' not in logout_index.data
    
    # response=test_client.get('/logout')
    # assert response.status_code ==302
    # assert response.location.endswith('/login_signup')
    
    # with test_client.session_transaction() as session:
    #     assert 'username' not in session
      
    # response=test_client.get('/login_signup')
    # assert response.status_code == 200  
    # assert b'Log In/Sign up' in test_client.get('login_signup').data
    
    
def test_user_delete(test_client):
    clear_db()
    test_user = AppUser(username='testuser', hashed_password='test_password')
    db.session.add(test_user)
    db.session.commit()


    test_client.post('/process_form', data={'username':'testuser', 'hashed_password':'test_password'})
    response = test_client.post('/delete_user')

    assert response.status_code == 200  
    assert b'Your account has been deleted successfully.' in response.data