from utils import heavily_populate_db, clear_db
from src.models import Post, Comment

# test viewing a single forum post
def test_view_single_forum_post(test_client):
    heavily_populate_db()

    # Create a post with a comment
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

    # View the single forum post
    response_view_single_post = test_client.get(f'/view_single_forum_post/{created_post.post_id}')

    assert response_view_single_post.status_code == 200

    # Logout
    with test_client.session_transaction() as session:
        del session['username']

