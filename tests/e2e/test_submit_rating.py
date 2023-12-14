from utils import clear_db, heavily_populate_db
from app import repository_singleton
from src.models import Rating

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
    
    clear_db()

# @app.post('/submit_rating')
def test_submit_rating_valid(test_client):
    heavily_populate_db()
    
    # simulate session
    with test_client.session_transaction() as session:
        session['username'] = 'user1'
    
    response = test_client.post('/submit_rating', data={
        'course': '1',
        'instructor': 'test',
        'quality': 1,
        'difficulty': 1,
        'grade': None,
        'description': "extremely unique description which nobody would just so happen to write (hopefully)"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert Rating.query.filter(Rating.description == "extremely unique description which nobody would just so happen to write (hopefully)").first() is not None

    # log out
    with test_client.session_transaction() as session:
        del session['username']
    
    clear_db()

def test_submit_rating_not_logged_in(test_client):
    heavily_populate_db()
    
    response = test_client.post('/submit_rating', data={
        'course': '1',
        'instructor': 'test',
        'quality': 1,
        'difficulty': 1,
        'grade': None,
        'description': None
    })
    
    assert response.status_code == 401
    
    clear_db()

def test_submit_rating_invalid_data(test_client):
    heavily_populate_db()
    # simulate session
    with test_client.session_transaction() as session:
        session['username'] = 'user1'
        
    # no course given
    response = test_client.post('/submit_rating', data={
        'course': None,
        'instructor': 'test',
        'quality': 1,
        'difficulty': 1,
        'grade': None,
        'description': None
    })
    assert response.status_code == 400
        
    # course doesn't exist
    response = test_client.post('/submit_rating', data={
        'course': 20,
        'instructor': 'test',
        'quality': 1,
        'difficulty': 1,
        'grade': None,
        'description': None
    })
    assert response.status_code == 400
    
    # no instructor given
    response = test_client.post('/submit_rating', data={
        'course': '1',
        'instructor': None,
        'quality': 1,
        'difficulty': 1,
        'grade': None,
        'description': None
    })
    assert response.status_code == 400
    
    # no quality given
    response = test_client.post('/submit_rating', data={
        'course': '1',
        'instructor': 'test',
        'quality': None,
        'difficulty': 1,
        'grade': None,
        'description': None
    })
    assert response.status_code == 400
    
    # quality less than 1
    response = test_client.post('/submit_rating', data={
        'course': '1',
        'instructor': 'test',
        'quality': 0,
        'difficulty': 1,
        'grade': None,
        'description': None
    })
    assert response.status_code == 400
    
    # quality more than 5
    response = test_client.post('/submit_rating', data={
        'course': '1',
        'instructor': 'test',
        'quality': 6,
        'difficulty': 1,
        'grade': None,
        'description': None
    })
    assert response.status_code == 400
    
    # no difficulty given
    response = test_client.post('/submit_rating', data={
        'course': '1',
        'instructor': 'test',
        'quality': None,
        'difficulty': 1,
        'grade': None,
        'description': None
    })
    assert response.status_code == 400
    
    # difficulty less than 1
    response = test_client.post('/submit_rating', data={
        'course': '1',
        'instructor': 'test',
        'quality': 1,
        'difficulty': 0,
        'grade': None,
        'description': None
    })
    assert response.status_code == 400
    
    # difficulty more than 5
    response = test_client.post('/submit_rating', data={
        'course': '1',
        'instructor': 'test',
        'quality': 1,
        'difficulty': 6,
        'grade': None,
        'description': None
    })
    assert response.status_code == 400
    
    # invalid grade
    response = test_client.post('/submit_rating', data={
        'course': '1',
        'instructor': 'test',
        'quality': 1,
        'difficulty': 1,
        'grade': 'E',
        'description': None
    })
    assert response.status_code == 400
    
    # log out
    with test_client.session_transaction() as session:
        del session['username']
        
    clear_db()