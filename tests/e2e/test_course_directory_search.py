from src.models import AppUser, Course, Rating, Post, Comment
from utils import clear_db, populate_db, heavily_populate_db

def test_search_status(test_client):
    response = test_client.get('/search')
    assert response.status_code == 200 #test if request succeeded

def test_search_content(test_client):
    response = test_client.get('/search')
    assert b'Choose one or more search criteria' in response.data #tests if search page content is shown
    assert b'Sort By Class Quality Rating' in response.data
    assert b'Sort By Class Difficulty Rating' in response.data
    assert b'Sort By Credit Hours' in response.data

def test_search_forms(test_client):
    populate_db()
    response = test_client.post('/search', data={'major': 'Computer Science'}, follow_redirects=True) #tests if forms are functioning
    assert response.status_code == 200

    response = test_client.post('/search', data={'quality': 'Quality3Plus'}, follow_redirects=True)
    assert response.status_code == 200

    response = test_client.post('/search', data={'difficulty': 'Diff4Plus'}, follow_redirects=True)
    assert response.status_code == 200

    response = test_client.post('/search', data={'credit': 4}, follow_redirects=True)
    assert response.status_code == 200

def test_search_empty(test_client):
    populate_db()
    response = test_client.post('/search', data={'major': ''}, follow_redirects=True) #when no search parameters are entered/forms are not filled out
    assert response.status_code == 200

    response = test_client.post('/search', data={'quality': ''}, follow_redirects=True)
    assert response.status_code == 200

    response = test_client.post('/search', data={'difficulty': ''}, follow_redirects=True)
    assert response.status_code == 200

    response = test_client.post('/search', data={'credit': ''}, follow_redirects=True)
    assert response.status_code == 200



