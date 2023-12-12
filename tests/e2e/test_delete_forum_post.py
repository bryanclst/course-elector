from utils import heavily_populate_db
from app import repository_singleton
from src.models import Post

# test a successful post deletion
def test_successfully_delete_post(test_client):
    heavily_populate_db()

    # create a post
    with test_client.session_transaction() as session:
        session['username'] = 'user1'
    
    response_create = test_client.post('/create_forum_post', data={
        'subject': 'hello!',
        'body': 'test post',
        'course_id': 1,
    }, follow_redirects=True)

    #make sure the post exists...
    assert response_create.status_code == 200
    assert Post.query.filter(Post.body == "test post").first() is not None

    #now delete it
    created_post = Post.query.filter(Post.body == "test post").first()
    response_delete = test_client.get(f'/delete_post/{created_post.post_id}', follow_redirects=True)

    assert response_delete.status_code == 200
    assert Post.query.get(created_post.post_id) is None

    # log out
    with test_client.session_transaction() as session:
        del session['username']

def test_delete_post_not_logged_in(test_client):
    heavily_populate_db()

    #LOG IN FIRST!
    with test_client.session_transaction() as session:
        session['username'] = 'user1'

    # create a post
    response_create = test_client.post('/create_forum_post', data={
        'subject': 'hello!',
        'body': 'test post',
        'course_id': 1,
    }, follow_redirects=True)

    assert response_create.status_code == 200
    created_post = Post.query.filter(Post.body == "test post").first()
    assert created_post is not None

    #NOW log out smh
    with test_client.session_transaction() as session:
        del session['username']

    # attempt to delete the post when not logged in
    response_delete = test_client.get(f'/delete_post/{created_post.post_id}', follow_redirects=True)

    assert response_delete.status_code == 401

# test attempting to edit a post with mismatched author ID
def test_edit_post_that_isnt_users(test_client):
    heavily_populate_db()

    # create a post
    with test_client.session_transaction() as session:
        session['username'] = 'user1'
    
    response_create = test_client.post('/create_forum_post', data={
        'subject': 'hello!',
        'body': 'test post',
        'course_id': 1,
    }, follow_redirects=True)

    assert response_create.status_code == 200
    created_post = Post.query.filter(Post.body == "test post").first()
    assert created_post is not None

    # log in as a different user
    with test_client.session_transaction() as session:
        session['username'] = 'user2'

    # attempt to delete the post with mismatched author ID
    response_delete = test_client.get(f'/delete_post/{created_post.post_id}', follow_redirects=True)

    assert response_delete.status_code == 403

    with test_client.session_transaction() as session:
        del session['username']
