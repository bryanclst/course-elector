from src.models import AppUser, Course, Rating, Post, Comment, db
from utils import clear_db, populate_db, heavily_populate_db, users_db

def test_users_db(test_client):
    users_db()

    user1 = AppUser.query.filter_by(username='user1').first()
    user2 = AppUser.query.filter_by(username='user2').first()

    assert user1 is not None
    assert user1.email == 'user1@example.com'
    assert user1.hashed_password == 'hashed_password_1'

    assert user2 is not None
    assert user2.email == 'user2@example.com'
    assert user2.hashed_password == 'hashed_password_2'

    all_users = AppUser.query.all()
    assert len(all_users) == 2


from utils import clear_db, populate_db, heavily_populate_db, courses_db

def test_clear_db(test_client):
    clear_db() # i have no idea how to test this without actually clearing the database and resetting serial keys first, but i think it's fine
    
    user = AppUser(email='user1@example.com', username='user1', hashed_password='hashed_password_1')
    course = Course(course_letter='COMP', course_number=1101, title='Introduction to Computer Science', credits=3, major='Computer Science')
    rating = Rating(course=course, author=user, instructor='Prof. Smith', quality=4, difficulty=3, grade='A', description='Great course!')
    post = Post(course=course, author=user, subject='Question about Assignment 1', body='I need help with question 3. Any suggestions?')
    comment = Comment(post=post, author=user, body="Sure! I had trouble with that too. Let's discuss it.")
    db.session.add_all([user, course, rating, post, comment])
    db.session.commit()
    
    # verify that data is in database; rating/comment existing covers all the tables
    ratings = Rating.query.all()
    assert len(ratings) == 1
    comments = Comment.query.all()
    assert len(comments) == 1
    
    clear_db()
    
    # there should be no users or courses, which all other tables depend on
    users = AppUser.query.all()
    assert len(users) == 0
    courses = Course.query.all()
    assert len(courses) == 0
    
    # if i add a new user, it should be id 1
    user = AppUser(email='user1@example.com', username='user1', hashed_password='hashed_password_1')
    db.session.add(user)
    db.session.commit()
    
    users = AppUser.query.all()
    assert len(ratings) == 1
    assert users[0].user_id == 1
    
    clear_db()

def test_populate_db(test_client):
    populate_db()
    
    users = AppUser.query.all()
    assert len(users) == 2
    assert users[0].username == 'user1'
    
    courses = Course.query.all()
    assert len(courses) == 2
    assert courses[1].course_letter == 'MATH'
    
    ratings = Rating.query.all()
    assert len(ratings) == 2
    assert ratings[1].quality == 3
    
    posts = Post.query.all()
    assert len(posts) == 2
    assert posts[0].author_id == 1
    
    comments = Comment.query.all()
    assert len(comments) == 2
    assert comments[0].post_id == 1
    
    clear_db()
    populate_db() # testing serial reset
    
    users = AppUser.query.all()
    assert users[0].user_id == 1
    courses = Course.query.all()
    assert courses[0].course_id == 1
    ratings = Rating.query.all()
    assert ratings[0].rating_id == 1
    posts = Post.query.all()
    assert posts[0].post_id == 1
    comments = Comment.query.all()
    assert comments[0].comment_id == 1
    
    clear_db()

def test_heavily_populate_db(test_client):
    heavily_populate_db()
    
    users = AppUser.query.all()
    assert len(users) == 2
    
    courses = Course.query.all()
    assert len(courses) == 15
    
    ratings = Rating.query.all()
    assert len(ratings) == 15
    
    posts = Post.query.all()
    assert len(posts) == 5
    
    comments = Comment.query.all()
    assert len(comments) == 5
    
    clear_db()
    heavily_populate_db() # testing serial reset
    
    users = AppUser.query.all()
    assert users[0].user_id == 1
    courses = Course.query.all()
    assert courses[0].course_id == 1
    ratings = Rating.query.all()
    assert ratings[0].rating_id == 1
    posts = Post.query.all()
    assert posts[0].post_id == 1
    comments = Comment.query.all()
    assert comments[0].comment_id == 1
    
    clear_db()

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

    clear_db()

