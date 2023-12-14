from utils import heavily_populate_db, clear_db
from src.models import Post

# test a successful post edit
def test_edit_valid_post(test_client):
    heavily_populate_db()

    # create a post
    with test_client.session_transaction() as session:
        session['username'] = 'user1'

    response_create_post = test_client.post('/create_forum_post', data={
        'subject': 'hello!',
        'body': 'test post',
        'course_id': 1,
    }, follow_redirects=True)

    assert response_create_post.status_code == 200
    created_post = Post.query.filter(Post.body == "test post").first()
    assert created_post is not None

    # edit the created post
    response_edit_post = test_client.post(f'/edit_post/{created_post.post_id}', data={
        'subject': 'edited subject',
        'body': 'edited body',
        'course_id': 2,
    }, follow_redirects=True)

    assert response_edit_post.status_code == 200
    edited_post = Post.query.get(created_post.post_id)
    assert edited_post is not None
    assert edited_post.subject == 'edited subject'
    assert edited_post.body == 'edited body'
    assert edited_post.course_id == 2

    with test_client.session_transaction() as session:
        del session['username']
    clear_db()

# test editing a post with bad data
def test_edit_post_with_invalid_data(test_client):
    heavily_populate_db()

    # create a post
    with test_client.session_transaction() as session:
        session['username'] = 'user1'

    response_create_post = test_client.post('/create_forum_post', data={
        'subject': 'hello!',
        'body': 'test post',
        'course_id': 1,
    }, follow_redirects=True)

    assert response_create_post.status_code == 200
    created_post = Post.query.filter(Post.body == "test post").first()
    assert created_post is not None

    # Bad subject data
    response_edit_post = test_client.post(f'/edit_post/{created_post.post_id}', data={
        'subject': None,
        'body': 'edited body',
        'course_id': 2,
    }, follow_redirects=True)

    assert response_edit_post.status_code == 400

    #bad body data
    response_edit_post = test_client.post(f'/edit_post/{created_post.post_id}', data={
        'subject': 'edited subject',
        'body': None,
        'course_id': 2,
    }, follow_redirects=True)
    assert response_edit_post.status_code == 400

    #Course doesn't exist or isn't in the list
    response_edit_post = test_client.post(f'/edit_post/{created_post.post_id}', data={
        'subject': 'edited subject',
        'body': 'edited body',
        'course_id': 999,
    }, follow_redirects=True)
    assert response_edit_post.status_code == 400

    response_edit_post = test_client.post(f'/edit_post/{created_post.post_id}', data={
        'subject': 'edited subject',
        'body': 'edited body',
        'course_id': None,
    }, follow_redirects=True)
    assert response_edit_post.status_code == 400

    with test_client.session_transaction() as session:
        del session['username']
    clear_db()

# test attempting to edit a post while not logged in
def test_edit_post_not_logged_in(test_client):
    heavily_populate_db()

    # create a post
    with test_client.session_transaction() as session:
        session['username'] = 'user1'

    response_create_post = test_client.post('/create_forum_post', data={
        'subject': 'hello!',
        'body': 'test post',
        'course_id': 1,
    }, follow_redirects=True)

    assert response_create_post.status_code == 200
    created_post = Post.query.filter(Post.body == "test post").first()
    assert created_post is not None

    # log out
    with test_client.session_transaction() as session:
        del session['username']

    # attempt to edit the post while not logged in
    response_edit_post = test_client.post(f'/edit_post/{created_post.post_id}', data={
        'subject': 'edited subject',
        'body': 'edited body',
        'course_id': 2,
    }, follow_redirects=True)

    assert response_edit_post.status_code == 401
    clear_db()

def test_editing_post_that_isnt_users(test_client):
    heavily_populate_db()

    # create a post
    with test_client.session_transaction() as session:
        session['username'] = 'user1'

    response_create_post = test_client.post('/create_forum_post', data={
        'subject': 'hello!',
        'body': 'test post',
        'course_id': 1,
    }, follow_redirects=True)

    assert response_create_post.status_code == 200
    created_post = Post.query.filter(Post.body == "test post").first()
    assert created_post is not None

    # log in as a different user
    with test_client.session_transaction() as session:
        session['username'] = 'user2'

    # attempt to edit the post with mismatched author ID
    response_edit_post = test_client.post(f'/edit_post/{created_post.post_id}', data={
        'subject': 'edited subject',
        'body': 'edited body',
        'course_id': 2,
    }, follow_redirects=True)

    assert response_edit_post.status_code == 403

    with test_client.session_transaction() as session:
        del session['username']
    clear_db()
    
    
