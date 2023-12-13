from src.repositories.repository import repository_singleton
from src.models import AppUser, Course, db
from utils import clear_db, heavily_populate_db

def test_get_user_by_username(test_client):
    clear_db()
    
    user1 = AppUser(email='user1@example.com', username='user1', hashed_password='hashed_password_1')
    user2 = AppUser(email='user2@example.com', username='user2', hashed_password='hashed_password_2')
    db.session.add_all([user1, user2])
    db.session.commit()
    
    queried_user1 = repository_singleton.get_user_by_username('user1')
    assert queried_user1
    assert queried_user1.username == user1.username
    assert queried_user1.email == user1.email
    assert queried_user1.hashed_password == user1.hashed_password
    
    queried_user2 = repository_singleton.get_user_by_username('user2')
    assert queried_user2
    assert queried_user2.username == user2.username
    assert queried_user2.email == user2.email
    assert queried_user2.hashed_password == user2.hashed_password
    
    queried_user3 = repository_singleton.get_user_by_username('user3')
    assert not queried_user3
    
    clear_db()

def test_get_user_by_id(test_client):
    clear_db()
    
    user1 = AppUser(email='user1@example.com', username='user1', hashed_password='hashed_password_1')
    user2 = AppUser(email='user2@example.com', username='user2', hashed_password='hashed_password_2')
    db.session.add_all([user1, user2])
    db.session.commit()
    
    queried_user1 = repository_singleton.get_user_by_id(1)
    assert queried_user1
    assert queried_user1.username == user1.username
    assert queried_user1.email == user1.email
    assert queried_user1.hashed_password == user1.hashed_password
    
    queried_user2 = repository_singleton.get_user_by_id(2)
    assert queried_user2
    assert queried_user2.username == user2.username
    assert queried_user2.email == user2.email
    assert queried_user2.hashed_password == user2.hashed_password
    
    queried_user3 = repository_singleton.get_user_by_id(3)
    assert not queried_user3
    
    clear_db()
    
    
def test_get_all_courses(test_client):
    clear_db()
    
    course1 = Course(course_letter='ITSC', course_number=1001, title='Course 1', credits=3, major='Computer Science')
    course2 = Course(course_letter='MATH', course_number=1002, title='Course 2', credits=4, major='Mathematics')
    db.session.add_all([course1, course2])
    db.session.commit()
    
    courses = repository_singleton.get_all_courses()
    assert len(courses) == 2
    assert courses[0].course_id == 1
    assert courses[0].course_letter == 'ITSC'
    assert courses[0].course_number == 1001
    assert courses[0].title == 'Course 1'
    assert courses[0].credits == 3
    assert courses[0].major == 'Computer Science'
    
    assert courses[1].course_id == 2
    assert courses[1].course_letter == 'MATH'
    assert courses[1].course_number == 1002
    assert courses[1].title == 'Course 2'
    assert courses[1].credits == 4
    assert courses[1].major == 'Mathematics'
    
    clear_db()

def test_get_course_by_id(test_client):
    clear_db()
    
    course1 = Course(course_letter='ITSC', course_number=1001, title='Course 1', credits=3, major='Computer Science')
    course2 = Course(course_letter='MATH', course_number=1002, title='Course 2', credits=4, major='Mathematics')
    db.session.add_all([course1, course2])
    db.session.commit()
    
    queried_course1 = repository_singleton.get_course_by_id(1)
    assert queried_course1.course_letter == 'ITSC'
    assert queried_course1.course_number == 1001
    assert queried_course1.title == 'Course 1'
    assert queried_course1.credits == 3
    assert queried_course1.major == 'Computer Science'
    
    queried_course2 = repository_singleton.get_course_by_id(2)
    assert queried_course2.course_id == 2
    assert queried_course2.course_letter == 'MATH'
    assert queried_course2.course_number == 1002
    assert queried_course2.title == 'Course 2'
    assert queried_course2.credits == 4
    assert queried_course2.major == 'Mathematics'
    
    queried_course3 = repository_singleton.get_course_by_id(3)
    assert not queried_course3
    
    clear_db()

def test_get_ratings_by_course(test_client):
    heavily_populate_db()
    
    ratings = repository_singleton.get_ratings_by_course_id(2)
    assert len(ratings) == 3
    
    assert ratings[0].rating_id == 2
    assert ratings[0].difficulty == 2
    
    assert ratings[1].rating_id == 3
    assert ratings[1].instructor == 'Prof. Johnson'
    
    assert ratings[2].rating_id == 9
    assert ratings[2].grade == 'B'
    
    ratings = repository_singleton.get_ratings_by_course_id(12)
    assert not ratings
    
    clear_db()

def test_create_rating(test_client):
    heavily_populate_db()
    
    ratings = repository_singleton.get_ratings_by_course_id(15)
    assert not ratings
    
    repository_singleton.create_rating(15, 1, 'person', 1, 5, 'F', 'asdf')
    ratings = repository_singleton.get_ratings_by_course_id(15)
    assert len(ratings) == 1
    assert ratings[0].rating_id == 16
    assert ratings[0].course_id == 15
    assert ratings[0].author_id == 1
    assert ratings[0].instructor == 'person'
    assert ratings[0].quality == 1
    assert ratings[0].difficulty == 5
    assert ratings[0].grade == 'F'
    assert ratings[0].description == 'asdf'
    
    ratings = repository_singleton.get_ratings_by_course_id(14)
    assert not ratings
    
    repository_singleton.create_rating(14, 2, 'person2', 5, 1) # no grade or description
    ratings = repository_singleton.get_ratings_by_course_id(14)
    assert len(ratings) == 1
    assert ratings[0].rating_id == 17
    assert ratings[0].course_id == 14
    assert ratings[0].author_id == 2
    assert ratings[0].instructor == 'person2'
    assert ratings[0].quality == 5
    assert ratings[0].difficulty == 1
    assert ratings[0].grade == None
    assert ratings[0].description == None
    
    clear_db()
    
    # tests for submitting invalid rating data do exist, but the logic is no in create_rating(). instead, it's in app.py and is tested in the e2e tests