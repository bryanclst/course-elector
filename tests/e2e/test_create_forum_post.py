from utils import heavily_populate_db, clear_db
from src.models import Post

# test a successful post creation
def test_create_valid_post(test_client):
    heavily_populate_db()
    
    # simulate session
    with test_client.session_transaction() as session:
        session['username'] = 'user1'
    
    response = test_client.post('/create_forum_post', data={
        'subject': 'hello!',
        'body': 'test post',
        'course_id': 1,
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert Post.query.filter(Post.body == "test post").first() is not None

    # log out
    with test_client.session_transaction() as session:
        del session['username']
    clear_db()

#test creating a post while a session is not active (user isn't logged in)
def test_create_post_not_logged_in(test_client):
    heavily_populate_db()
    
    response = test_client.post('/create_forum_post', data={
        'subject': 'hello!',
        'body': 'test post',
        'course_id': 1,
    }, follow_redirects=True)
    
    assert response.status_code == 401
    clear_db()

#test various forms of bad data
def test_create_post_with_invalid_data(test_client):
    heavily_populate_db()
    # simulate session
    with test_client.session_transaction() as session:
        session['username'] = 'user1'
        
    #no subject given
    response = test_client.post('/create_forum_post', data={
        'subject': None,
        'body': 'test post',
        'course_id': 1,
    }, follow_redirects=True)
    assert response.status_code == 400

    #no body given
    response = test_client.post('/create_forum_post', data={
        'subject': 'hi!',
        'body': None,
        'course_id': 1,
    }, follow_redirects=True)
    assert response.status_code == 400

    #no course id given
    response = test_client.post('/create_forum_post', data={
        'subject': 'hi!',
        'body': 'test post',
        'course_id': None,
    }, follow_redirects=True)
    assert response.status_code == 400

    #course ID doesn't exist
    response = test_client.post('/create_forum_post', data={
        'subject': 'hi!',
        'body': 'test post',
        'course_id': 999,
    }, follow_redirects=True)
    assert response.status_code == 400

    # log out
    with test_client.session_transaction() as session:
        del session['username']
    clear_db()
    