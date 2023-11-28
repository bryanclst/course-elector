from src.models import AppUser, Course, Rating, Post, Comment, db

class Repository:
    def get_all_users(self):
        return AppUser.query.all()
    
    def get_user_by_username(self, username):
        return AppUser.query.filter_by(username=username).first()
    
    def get_all_courses(self):
        return Course.query.all()
    
    def get_course_by_id(self, course_id: int):
        return Course.query.filter_by(course_id=course_id).first()
    
    def get_all_ratings(self):
        return Rating.query.all()
    
    def get_ratings_by_course(self, course_id: int):
        return Rating.query.filter_by(course_id=course_id).all()
    
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