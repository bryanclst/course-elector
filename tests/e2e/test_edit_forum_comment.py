from utils import heavily_populate_db
from src.models import Post, Comment

# test a successful comment edit
def test_edit_valid_comment(test_client):
    heavily_populate_db()

    # create a post with a comment
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

    response_create_comment = test_client.post(f'/create_forum_comment/{created_post.post_id}', data={
        'body': 'test comment',
    }, follow_redirects=True)

    assert response_create_comment.status_code == 200
    created_comment = Comment.query.filter(Comment.body == "test comment").first()
    assert created_comment is not None

    # edit the created comment
    response_edit_comment = test_client.post(f'/edit_comment/{created_post.post_id}/{created_comment.comment_id}', data={
        'body': 'edited comment',
    }, follow_redirects=True)

    assert response_edit_comment.status_code == 200
    edited_comment = Comment.query.get(created_comment.comment_id)
    assert edited_comment is not None
    assert edited_comment.body == 'edited comment'
    with test_client.session_transaction() as session:
        del session['username']

# test editing a comment with bad data
def test_edit_comment_with_invalid_data(test_client):
    heavily_populate_db()

    # create a post with a comment
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

    response_create_comment = test_client.post(f'/create_forum_comment/{created_post.post_id}', data={
        'body': 'test comment',
    }, follow_redirects=True)

    assert response_create_comment.status_code == 200
    created_comment = Comment.query.filter(Comment.body == "test comment").first()
    assert created_comment is not None

    # edit the created comment, now with bad Body data
    response_edit_comment = test_client.post(f'/edit_comment/{created_post.post_id}/{created_comment.comment_id}', data={
        'body': None,
    }, follow_redirects=True)

    assert response_edit_comment.status_code == 400
    with test_client.session_transaction() as session:
        del session['username']
    
# test attempting to edit a comment while not logged in
def test_edit_comment_not_logged_in(test_client):
    heavily_populate_db()

    # create a post with a comment
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

    response_create_comment = test_client.post(f'/create_forum_comment/{created_post.post_id}', data={
        'body': 'test comment',
    }, follow_redirects=True)

    assert response_create_comment.status_code == 200
    created_comment = Comment.query.filter(Comment.body == "test comment").first()
    assert created_comment is not None

    # log out
    with test_client.session_transaction() as session:
        del session['username']

    # attempt to edit the comment while not logged in
    response_edit_comment = test_client.post(f'/edit_comment/{created_post.post_id}/{created_comment.comment_id}', data={
        'body': 'edited comment',
    }, follow_redirects=True)

    assert response_edit_comment.status_code == 401

# test attempting to edit a comment not belonging to the logged-in user
def test_edit_comment_that_isnt_users(test_client):
    heavily_populate_db()

    # create a post with a comment
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

    response_create_comment = test_client.post(f'/create_forum_comment/{created_post.post_id}', data={
        'body': 'test comment',
    }, follow_redirects=True)

    assert response_create_comment.status_code == 200
    created_comment = Comment.query.filter(Comment.body == "test comment").first()
    assert created_comment is not None

    # log in as a different user
    with test_client.session_transaction() as session:
        session['username'] = 'user2'

    # attempt to edit the comment with mismatched author ID
    response_edit_comment = test_client.post(f'/edit_comment/{created_post.post_id}/{created_comment.comment_id}', data={
        'body': 'edited comment',
    }, follow_redirects=True)

    assert response_edit_comment.status_code == 403
    with test_client.session_transaction() as session:
        del session['username']
    
