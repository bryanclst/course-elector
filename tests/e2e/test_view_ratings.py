from utils import heavily_populate_db, clear_db

# @app.get('/view_ratings/<int:course_id>')
def test_no_ratings(test_client):
    heavily_populate_db()
    
    response = test_client.get('/view_ratings/15')
    assert response.status_code == 200
    
    data = response.data.decode()
    assert '<h1>No ratings for this course</h1>' in data
    assert '<div class="ratings-container">' not in data
    
    clear_db()

def test_view_ratings(test_client):
    heavily_populate_db()
    
    response = test_client.get('/view_ratings/1')
    assert response.status_code == 200
    
    data = response.data.decode()
    assert '<h1>No ratings for this course</h1>' not in data
    assert '<div class="ratings-container">' in data
    
    clear_db()