from src.models import AppUser, Course, Rating, Post, Comment, db
from utils import clear_db, populate_db, heavily_populate_db, courses_db

def test_courses_db(test_client):
    courses_db()
    course1 = Course.query.filter_by(course_number=1212).first()
    course2 = Course.query.filter_by(course_number=2181).first()
    course3 = Course.query.filter_by(course_number=3111).first()
    assert course1 is not None
    assert course1.title == "Intro to Computer Science I"
    assert course1.major == "Computer Science"
    assert course2 is not None
    assert course2.title == "Intro To Computer Systems"
    assert course2.major == "Computer Science"
    assert course3 is not None
    assert course3.title == "Quantitative Analysis"
    assert course3.major == "Chemistry"
    
    all_courses = Course.query.all() 
    assert len(all_courses) == 31