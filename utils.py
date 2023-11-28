from src.models import AppUser, Course, Rating, Post, Comment, db
from sqlalchemy import text

def clear_db():
    Comment.query.delete()
    Post.query.delete()
    Rating.query.delete()
    Course.query.delete()
    AppUser.query.delete()
    db.session.commit()

def populate_db():
    clear_db()
    
    # # reset SERIAL auto increment
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