from src.models import AppUser, Course, Rating, Post, Comment, db

class Repository:
    def get_all_users(self):
        return AppUser.query.all()
    
    def get_all_courses(self):
        return Course.query.all()
    
    def get_all_ratings(self):
        return Rating.query.all()
    
    def create_rating(self, course_id, author_id, instructor, quality, difficulty, grade=None, description=None):
        new_rating = Rating(course_id=course_id, author_id=author_id, instructor=instructor, quality=quality, difficulty=difficulty, grade=grade, description=description)
        db.session.add(new_rating)
        db.session.commit()
        return new_rating
    
    def get_all_posts(self):
        return Post.query.all()
    
    def get_all_comments(self):
        return Comment.query.all()

repository_singleton = Repository()