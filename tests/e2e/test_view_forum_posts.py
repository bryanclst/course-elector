from utils import heavily_populate_db, clear_db
from src.models import Post

# test viewing forum posts
def test_view_forum_posts(test_client):
    heavily_populate_db()

    response = test_client.get('/view_forum_posts')

    #simple test to make sure it works
    assert response.status_code == 200
    assert b'CourseElector Forum Home' in response.data
    clear_db()