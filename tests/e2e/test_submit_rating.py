from src.models import AppUser, Course, Rating, Post, Comment
from utils import clear_db, populate_db, heavily_populate_db
from app import repository_singleton
from flask import session

# def test(test_client):
#     heavily_populate_db()
#     assert True

# @app.get('/submit_rating')
def test_get_submit_rating_page(test_client):
    heavily_populate_db()
    response = test_client.get('/submit_rating')
    assert response.status_code == 200

    data = response.data.decode()

    # check that all courses in database are options in the form
    courses = repository_singleton.get_all_courses()
    for course in courses:
        assert f'<option value="{course.course_id}">' in data


# @app.post('/submit_rating')
def test_submit_rating_valid(test_client):
    heavily_populate_db()
    with test_client.session_transaction() as session:
        session['username'] = 'user1'


    response = test_client.post('/submit_rating', data={
        'course': '1',
        'instructor': 'test',
        'quality': 1,
        'difficulty': 1,
        'grade': None,
        'description': None # unique description to identify rating
    }, follow_redirects=True)
    
    assert response.status_code == 200


    # data = response.data.decode()

# def test_submit_rating_not_logged_in(test_client):
#     response = test_client.post('/submit_rating', data={
#         'course_id': 1,
#         'instructor': 'test',
#         'quality': 1,
#         'difficulty': 1,
#         'grade': None,
#         'description': None
#     }, follow_redirects=True)
    
#     assert response.status_code == 401

# def test_submit_rating_invalid(test_client):
#     # no course, no instructor, no quality, no difficulty
#     pass

