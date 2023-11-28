import bcrypt
from flask import Flask, render_template, redirect, request, abort, url_for, session, flash
from src.models import db, AppUser, Course, Rating, Post, Comment
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError 
from dotenv import load_dotenv
import os

from src.repositories.repository import repository_singleton

load_dotenv()
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

app.secret_key= os.getenv('APP_SECRET_KEY', 'abc')

bcrypt = Bcrypt(app)
db.init_app(app)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/view_forum_posts')
def view_forum_posts():
    posts = Post.query.all()
    return render_template('view_forum_posts.html', posts=posts, forum_active = True)

@app.route('/create_forum_post', methods=['GET', 'POST'])
def create_forum_post():
    if request.method == 'POST':
        subject = request.form['subject']
        body = request.form['body']
        selected_course_id = request.form['course_id']

        course = Course.query.get(selected_course_id)
        if course is None:
            return render_template('create_forum_post.html', courses = Course.query.all(), forum_active = True)
        
        #author id is 1 for testing
        post = Post(subject=subject, body=body, course=course, author_id=1)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('view_forum_posts'))
    
    return render_template('create_forum_post.html', courses=Course.query.all(), forum_active = True)


@app.route('/view_single_forum_post/<int:post_id>', methods=['GET', 'POST'])
def view_single_forum_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_single_forum_post.html', post=post, forum_active=True)


@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('view_forum_posts'))


@app.route('/delete_comment/<int:post_id>/<int:comment_id>', methods=['POST'])
def delete_comment(post_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('view_single_forum_post', post_id=post_id))



@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_forum_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.subject = request.form['subject']
        post.body = request.form['body']
        post.course_id = request.form['course_id']
        db.session.commit()
        return redirect(url_for('view_forum_posts'))

    return render_template('edit_forum_post.html', post=post, courses=Course.query.all(), forum_active=True)

@app.route('/create_forum_comment/<int:post_id>', methods=['POST'])
def create_forum_comment(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        body = request.form['body']

        #author ID is 1 for testing purposes
        comment = Comment(body=body, post=post, author_id=1)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('view_single_forum_post', post_id=post_id))

@app.route('/edit_comment/<int:post_id>/<int:comment_id>', methods=['GET', 'POST'])
def edit_forum_comment(post_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if request.method == 'POST':
        comment.body = request.form['body']
        db.session.commit()
        return redirect(url_for('view_single_forum_post', post_id=post_id))

    return render_template('edit_forum_comment.html', comment=comment, post_id=post_id, forum_active=True)

@app.route('/login_signup')
def login_signup():
    return render_template('login_signup.html', login_active=True)

@app.route('/process_form', methods=['POST'])
def process_form():
    username = request.form.get('username')
    hashed_password = request.form.get('hashed_password')
    action = request.form.get('action')
    
    if not username or not hashed_password:
        flash('Please provide both username and password', 'error')
        return redirect('/login_signup')

    if action == 'Sign Up':
        bcrypt_password = bcrypt.generate_password_hash(hashed_password).decode()
        try:
            new_user = AppUser(username=username, hashed_password=bcrypt_password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash('Account created successfully', 'success')
            return redirect('/login_signup')
        except IntegrityError:
            db.session.rollback()  # Rollback the transaction
            flash('Username already exists. Please choose another one.', 'error')
            return redirect('/login_signup')
    elif action == 'Login':
        existing_user = AppUser.query.filter_by(username=username).first()
        if not existing_user or not bcrypt.check_password_hash(existing_user.hashed_password, hashed_password):
            flash('Incorrect username or password', 'error')
            return redirect('/login_signup')
        session['username'] = username
        return redirect('/user_profile')
    else:
        return 'Invalid action'

@app.route('/user_profile')
def userprofile():
    username = session.get('username')
    
    if username is None:
        # Redirect to login page or handle unauthorized access
        return redirect('/login_signup')     
    
    return render_template('user_profile.html', username=session['username'], user_active=True)

@app.get('/submit_rating')
def get_rating_form():
    courses = repository_singleton.get_all_courses()
    return render_template('submit_rating.html', rating_active=True, courses=courses)

@app.post('/submit_rating')
def submit_rating():
    course_id = request.form.get('course')
    instructor = request.form.get('instructor')
    quality = request.form.get('quality')
    difficulty = request.form.get('difficulty')
    if course_id is None or instructor is None or quality is None or difficulty is None:
        abort(400)
    grade = request.form.get('grade')
    description = request.form.get('description')
    
    repository_singleton.create_rating(course_id=course_id, author_id=2, instructor=instructor, quality=quality, difficulty=difficulty, grade=grade, description=description)
    
    return redirect(f'/view_ratings/{course_id}') # TODO change to append the id of the course

@app.get('/view_ratings/<int:course_id>') # TODO variable to access specific id
def view_ratings(course_id):
    course = repository_singleton.get_course_by_id(course_id)
    if course is None:
        abort(400) # invalid course_id
        
    ratings = repository_singleton.get_ratings_by_course(course_id)
    if ratings is not None:
        qualities = [rating.quality for rating in ratings]
        avg_quality = round(sum(qualities) / len(qualities), 2)
        difficulties = [rating.difficulty for rating in ratings]
        avg_difficulty = round(sum(difficulties) / len(difficulties), 2)
    return render_template('view_ratings.html', rating_active=True, course=course, ratings=ratings, avg_quality=avg_quality, avg_difficulty=avg_difficulty)

if __name__ == '__main__':
    app.run(debug=True)

@app.get('/about')
def about_us():
    #Nick
    return render_template('about_us.html', about_active=True)

@app.get('/search')
def get_search():
    #Nick
    return render_template('course_directory_search.html', course_active=True)

@app.post('/search') #handles submissions
def post_search():
    #Nick
    major_choice = request.form.get('major') #getting form data from course_directory_search.html
    quality_choice = request.form.get('quality') 
    difficulty_choice = request.form.get('difficulty') 
    instructor_choice = request.form.get('instructorID')

    query_parameters = f'major={major_choice}&quality={quality_choice}&difficulty={difficulty_choice}&instructorID={instructor_choice}' # query in string format, so that the information gained from the forms can be used in course_directory()
    
    return redirect(f'/directory?{query_parameters}') #redirects to /directory with the appropriate query parameters that contain the data from the forms 


@app.get('/directory')
def course_directory():
    #Nick
    major_choice = request.args.get('major') #getting the data from the url query parameter
    quality_choice = request.args.get('quality') 
    difficulty_choice = request.args.get('difficulty') 
    instructor_choice = request.args.get('instructorID')

    #implement way to get list of courses based upon search parameters

    return render_template('course_directory.html', major_choice=major_choice, course_active=True) #would in theory be feeding in list of courses, just using major_choice for testing


