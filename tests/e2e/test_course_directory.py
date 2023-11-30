from src.models import AppUser, Course, Rating, Post, Comment
from utils import clear_db, populate_db, heavily_populate_db

def test_directory_populated(test_client):
    heavily_populate_db()
    course1 = Course.query.filter_by(course_number=1010).first()
    course2 = Course.query.filter_by(course_number=1001).first()
    course3 = Course.query.filter_by(course_number=1015).first()
    assert course1 is not None
    assert course2 is not None
    assert course3 is not None

def test_directory_empty(test_client):
    heavily_populate_db()
    clear_db()
    course = Course.query.filter_by(course_number=1010).first()
    assert course is None

    response = test_client.get('/directory')
    data = response.data.decode()
    assert b'No Classes matched description!' in response.data #this message is displayed only when there are no courses
    assert b'Difficulty Rating' not in response.data #only displayed when course table is populated

def test_directory_pagination(test_client):
    heavily_populate_db()
    response = test_client.get('/directory?page=3&page=2')
    assert b'MATH-1011' in response.data #this course should appear on the third page

def test_directory_filtering(test_client):
    heavily_populate_db()
    response = test_client.get('/directory?quality=Quality5Only')
    assert b'ITCS-1015' in response.data #this course is the only one in the test data with a quality 5 rating


def test_directory_filtering_multiple(test_client):
    heavily_populate_db()
    response = test_client.get('/directory?major=Mathematics&quality=Quality3Plus&difficulty=Diff4Plus&credit=4')
    assert b'ITCS-1014' in response.data #this course is the only one in the test data with these parameters
    assert b'ITCS-1015' not in response.data



def test_directory_filtering_and_rating_implementation(test_client):
    heavily_populate_db()
    response = test_client.get('/directory?quality=Quality4Plus')
    assert b'View Page' in response.data 
    assert b'No Page Yet' not in response.data