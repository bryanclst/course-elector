from utils import heavily_populate_db, clear_db
from src.models import Comment

# test a successful post creation
def test_create_valid_comment(test_client):
    heavily_populate_db()
    
    # simulate session
    with test_client.session_transaction() as session:
        session['username'] = 'user1'
    
    response = test_client.post('/create_forum_comment/1', data={
        'body': 'test comment',
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert Comment.query.filter(Comment.body == "test comment").first() is not None

    # log out
    with test_client.session_transaction() as session:
        del session['username']
    clear_db()
    

#test creating a comment while a session is not active (user isn't logged in)
def test_create_post_not_logged_in(test_client):
    heavily_populate_db()
    
    response = test_client.post('/create_forum_comment/1', data={
        'body': 'test comment',
    }, follow_redirects=True)
    
    assert response.status_code == 401
    clear_db()

#test with bad data
def test_create_comment_with_invalid_data(test_client):
    heavily_populate_db()
    # simulate session
    with test_client.session_transaction() as session:
        session['username'] = 'user1'
        
    #no body given
    response = test_client.post('/create_forum_comment/1', data={
        'body': 'test comment',
    }, follow_redirects=True)

    
    # log out
    with test_client.session_transaction() as session:
        del session['username']
    clear_db()