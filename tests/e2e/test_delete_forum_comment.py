from utils import heavily_populate_db
from app import repository_singleton
from src.models import Comment, Post

def test_successfully_delete_comment(test_client):
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

    # delete the created comment
    response_delete_comment = test_client.post(f'/delete_comment/{created_post.post_id}/{created_comment.comment_id}', follow_redirects=True)

    assert response_delete_comment.status_code == 200
    assert Comment.query.get(created_comment.comment_id) is None

    with test_client.session_transaction() as session:
        del session['username']

# test attempting to delete a comment when not logged in
def test_delete_comment_not_logged_in(test_client):
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

    # attempt to delete the comment when not logged in
    response_delete_comment = test_client.post(f'/delete_comment/{created_post.post_id}/{created_comment.comment_id}', follow_redirects=True)

    assert response_delete_comment.status_code == 401

# test attempting to delete a comment that doesn't belong to the logged-in user
def test_delete_comment_that_isnt_users(test_client):
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

    # attempt to delete the comment with mismatched author ID
    response_delete_comment = test_client.post(f'/delete_comment/{created_post.post_id}/{created_comment.comment_id}', follow_redirects=True)

    assert response_delete_comment.status_code == 403

    # log out
    with test_client.session_transaction() as session:
        del session['username']

