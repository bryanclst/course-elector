from src.models import AppUser, Course, Rating, Post, Comment, db
from sqlalchemy import text
import random

def clear_db():
    Comment.query.delete()
    Post.query.delete()
    Rating.query.delete()
    Course.query.delete()
    AppUser.query.delete()
    db.session.commit()

    # reset SERIAL auto increment
    table_primary_key_mapping = {
            AppUser.__tablename__: 'user_id',
            Course.__tablename__: 'course_id',
            Rating.__tablename__: 'rating_id',
            Post.__tablename__: 'post_id',
            Comment.__tablename__: 'comment_id',
        }

    for table_name, primary_key_column in table_primary_key_mapping.items():
        # Reset the sequence for each SERIAL column
        db.session.execute(text(f"SELECT setval(pg_get_serial_sequence('{table_name}', '{primary_key_column}'), coalesce(max({primary_key_column}), 1), false) FROM {table_name}"))

def populate_db():
    clear_db()
    
    user1 = AppUser(email='user1@example.com', username='user1', hashed_password='hashed_password_1')
    user2 = AppUser(email='user2@example.com', username='user2', hashed_password='hashed_password_2')

    course1 = Course(course_letter='COMP', course_number=1101, title='Introduction to Computer Science', credits=3, major='Computer Science')
    course2 = Course(course_letter='MATH', course_number=1201, title='Calculus I', credits=4, major='Mathematics')

    rating1 = Rating(course=course1, author=user1, instructor='Prof. Smith', quality=4, difficulty=3, grade='A', description='Great course!')
    rating2 = Rating(course=course2, author=user2, instructor='Prof. Johnson', quality=3, difficulty=4, grade='B', description='Challenging but interesting')

    post1 = Post(course=course1, author=user1, subject='Question about Assignment 1', body='I need help with question 3. Any suggestions?')
    post2 = Post(course=course2, author=user2, subject='Midterm Review Session', body="Let's organize a review session for the upcoming midterm.")

    comment1 = Comment(post=post1, author=user2, body="Sure! I had trouble with that too. Let's discuss it.")
    comment2 = Comment(post=post1, author=user1, body="I found question 3 tricky as well. Let's work on it together.")
    
    db.session.add_all([user1, user2, course1, course2, rating1, rating2, post1, post2, comment1, comment2])
    db.session.commit()
    
def heavily_populate_db():
    clear_db()
    
        # Add 2 users
    user1 = AppUser(email='user1@example.com', username='user1', hashed_password='hashed_password_1')
    user2 = AppUser(email='user2@example.com', username='user2', hashed_password='hashed_password_2')

    # Add 15 courses
    courses = [
        Course(course_letter='ITSC', course_number=1001, title='Course 1', credits=3, major='Computer Science'),
        Course(course_letter='ITSC', course_number=1002, title='Course 2', credits=4, major='Mathematics'),
        Course(course_letter='ITSC', course_number=1003, title='Course 3', credits=3, major='Computer Science'),
        Course(course_letter='ITSC', course_number=1004, title='Course 4', credits=4, major='Mathematics'),
        Course(course_letter='ITIS', course_number=1005, title='Course 5', credits=3, major='Computer Science'),
        Course(course_letter='ITIS', course_number=1006, title='Course 6', credits=4, major='Mathematics'),
        Course(course_letter='ITIS', course_number=1007, title='Course 7', credits=3, major='Computer Science'),
        Course(course_letter='ITIS', course_number=1008, title='Course 8', credits=4, major='Mathematics'),
        Course(course_letter='MATH', course_number=1009, title='Course 9', credits=3, major='Computer Science'),
        Course(course_letter='MATH', course_number=1010, title='Course 10', credits=4, major='Mathematics'),
        Course(course_letter='MATH', course_number=1011, title='Course 11', credits=3, major='Computer Science'),
        Course(course_letter='MATH', course_number=1012, title='Course 12', credits=4, major='Mathematics'),
        Course(course_letter='ITCS', course_number=1013, title='Course 13', credits=3, major='Computer Science'),
        Course(course_letter='ITCS', course_number=1014, title='Course 14', credits=4, major='Mathematics'),
        Course(course_letter='ITCS', course_number=1015, title='Course 15', credits=3, major='Computer Science'),
    ]

    # Add 15 ratings
    ratings = [
        Rating(course=courses[0], author=user1, instructor='Prof. Smith', quality=4, difficulty=3, grade='A', description='Rating 1 description'),
        Rating(course=courses[2], author=user2, instructor='Prof. Johnson', quality=3, difficulty=4, grade='B', description='Rating 2 description'),
        Rating(course=courses[2], author=user1, instructor='Prof. Anderson', quality=5, difficulty=2, grade='A', description='Rating 3 description'),
        Rating(course=courses[3], author=user2, instructor='Prof. Smith', quality=3, difficulty=3, grade='C', description='Rating 4 description'),
        Rating(course=courses[4], author=user1, instructor='Prof. Johnson', quality=4, difficulty=2, grade='B', description='Rating 5 description'),
        Rating(course=courses[2], author=user2, instructor='Prof. Anderson', quality=2, difficulty=4, grade='B', description='Rating 6 description'),
        Rating(course=courses[6], author=user1, instructor='Prof. Smith', quality=4, difficulty=3, grade='A', description='Rating 7 description'),
        Rating(course=courses[7], author=user2, instructor='Prof. Johnson', quality=3, difficulty=4, grade='C', description='Rating 8 description'),
        Rating(course=courses[7], author=user1, instructor='Prof. Anderson', quality=5, difficulty=2, grade='A', description='Rating 9 description'),
        Rating(course=courses[7], author=user2, instructor='Prof. Smith', quality=3, difficulty=3, grade='C', description='Rating 10 description'),
        Rating(course=courses[7], author=user1, instructor='Prof. Johnson', quality=4, difficulty=2, grade='B', description='Rating 11 description'),
        Rating(course=courses[11], author=user2, instructor='Prof. Anderson', quality=2, difficulty=4, grade='B', description='Rating 12 description'),
        Rating(course=courses[12], author=user1, instructor='Prof. Smith', quality=4, difficulty=3, grade='A', description='Rating 13 description'),
        Rating(course=courses[13], author=user2, instructor='Prof. Johnson', quality=3, difficulty=4, grade='C', description='Rating 14 description'),
        Rating(course=courses[14], author=user1, instructor='Prof. Anderson', quality=5, difficulty=2, grade='A', description='Rating 15 description'),
    ]

    # Add 5 posts
    posts = [
        Post(course=courses[0], author=user1, subject='Post Subject 1', body='Post 1 body'),
        Post(course=courses[1], author=user2, subject='Post Subject 2', body='Post 2 body'),
        Post(course=courses[2], author=user1, subject='Post Subject 3', body='Post 3 body'),
        Post(course=courses[3], author=user2, subject='Post Subject 4', body='Post 4 body'),
        Post(course=courses[4], author=user1, subject='Post Subject 5', body='Post 5 body'),
    ]

    # Add 5 comments
    comments = [
        Comment(post=posts[3], author=user2, body='Comment 1 body'),
        Comment(post=posts[1], author=user1, body='Comment 2 body'),
        Comment(post=posts[2], author=user2, body='Comment 3 body'),
        Comment(post=posts[3], author=user1, body='Comment 4 body'),
        Comment(post=posts[3], author=user2, body='Comment 5 body'),
    ]

    # Add objects to the session
    db.session.add_all([user1, user2] + courses + ratings + posts + comments)

    # Commit the changes to the database
    db.session.commit()