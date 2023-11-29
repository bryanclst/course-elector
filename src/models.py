from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AppUser(db.Model):
    __tablename__ = 'app_user'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)

    # fk relationships
    comments = db.relationship('Comment', back_populates="author", cascade='all, delete-orphan') # parent
    ratings = db.relationship('Rating', back_populates="author", cascade='all, delete-orphan') # parent
    posts = db.relationship('Post', back_populates="author", cascade='all, delete-orphan') # parent

    def __repr__(self):
        return f"<AppUser(user_id={self.user_id}, email={self.email}, username={self.username}, hashed={self.hashed_password})>"

    def __str__(self):
        return f"AppUser(user_id={self.user_id}, email={self.email}, username={self.username} hashed={self.hashed_password})"


class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True)
    course_letter = db.Column(db.String(4), nullable=False)
    course_number = db.Column(db.SmallInteger, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    credits = db.Column(db.SmallInteger)
    major = db.Column(db.String(255))
    
    # fk relationship (you can't delete a course with our website but whatever)
    ratings = db.relationship('Rating', back_populates="course", cascade='all, delete-orphan') # parent
    
    posts = db.relationship('Post', back_populates="course", cascade='all, delete-orphan') # parent

    def __repr__(self):
        return f"<Course(course_id={self.course_id}, title={self.title})>"

    def __str__(self):
        return f"Course(course_id={self.course_id}, title={self.title})"


class Rating(db.Model):
    __tablename__ = 'rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    instructor = db.Column(db.String(255), nullable=False)
    quality = db.Column(db.SmallInteger, nullable=False)
    difficulty = db.Column(db.SmallInteger, nullable=False)
    grade = db.Column(db.String(1))
    description = db.Column(db.Text)
    
    # fk relationships
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    course = db.relationship('Course', back_populates='ratings') # child
    
    author_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), nullable=False)
    author = db.relationship('AppUser', back_populates='ratings') # child

    def __repr__(self):
        return f"<Rating(rating_id={self.rating_id}, course_id={self.course_id}, author_id={self.author_id})>"

    def __str__(self):
        return f"Rating(rating_id={self.rating_id}, course_id={self.course_id}, author_id={self.author_id})"


class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    
    # fk relationships
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    course = db.relationship('Course', back_populates='posts') # child
    
    author_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), nullable=False)
    author = db.relationship('AppUser', back_populates='posts') # child

    comments = db.relationship('Comment', back_populates="post", cascade='all, delete-orphan') # parent

    def __repr__(self):
        return f"<Post(post_id={self.post_id}, course_id={self.course_id}, author_id={self.author_id}, subject={self.subject})>"

    def __str__(self):
        return f"Post(post_id={self.post_id}, course_id={self.course_id}, author_id={self.author_id}, subject={self.subject})"


class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    post = db.relationship('Post', back_populates='comments') # child
    
    author_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id'), nullable=False)
    author = db.relationship('AppUser', back_populates='comments') # child

    def __repr__(self):
        return f"<Comment(comment_id={self.comment_id}, post_id={self.post_id}, author_id={self.author_id})>"

    def __str__(self):
        return f"Comment(comment_id={self.comment_id}, post_id={self.post_id}, author_id={self.author_id})"
