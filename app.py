import bcrypt
from flask import Flask, render_template as real_render_template, redirect, request, abort, url_for, flash, session, json
from src.models import db, AppUser, Course, Rating, Post, Comment
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError 
from dotenv import load_dotenv
import os
import traceback

from src.repositories.repository import repository_singleton

from sqlalchemy import func, cast, Float 
from sqlalchemy.orm import joinedload 
from flask_sqlalchemy import pagination #just added

load_dotenv()
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

app.secret_key= os.getenv('APP_SECRET_KEY', 'abc')

bcrypt = Bcrypt(app)
db.init_app(app)

# custom render_template to pass username into all routes
def render_template(*args, **kwargs):
    if 'username' not in kwargs:
        kwargs['username']= session.get('username')
    return real_render_template(*args, **kwargs,)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {str(e)}")
    return "Internal Server Error", 500


@app.get('/')
def index():
    return render_template('index.html')

@app.get('/view_forum_posts')
def view_forum_posts():
    disabled = False
    if session.get('username') is None:
        disabled = True
    posts = Post.query.all()
    return render_template('view_forum_posts.html', posts=posts, forum_active = True, disabled = disabled)

@app.route('/create_forum_post', methods=['GET', 'POST'])
def create_forum_post():
    disabled = False
    if session.get('username') is None:
        disabled = True
    if request.method == 'POST':
        subject = request.form['subject']
        body = request.form['body']
        selected_course_id = request.form['course_id']

        if subject is None or body is None or selected_course_id is None:
            abort(400)
        if repository_singleton.get_course_by_id(selected_course_id) is None:
            abort(400)
        username = session.get('username')
        if username is None:
            abort(401)
        else:
            author_id = repository_singleton.get_user_by_username(username).user_id

        course = Course.query.get(selected_course_id)
        if course is None:
            return render_template('create_forum_post.html', courses = Course.query.all(), forum_active = True, disabled = disabled)
        
        
        post = Post(subject=subject, body=body, course=course, author_id=author_id)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('view_forum_posts'))
    
    return render_template('create_forum_post.html', courses=Course.query.all(), forum_active = True, disabled=disabled)


@app.route('/view_single_forum_post/<int:post_id>', methods=['GET', 'POST'])
def view_single_forum_post(post_id):
    disabled = False
    if session.get('username') is None:
        disabled = True
    post = Post.query.get_or_404(post_id)
    post_author_id = post.author_id
    poster_username = repository_singleton.get_user_by_id(post_author_id).username

    comment_usernames = [repository_singleton.get_user_by_id(comment.author_id).username for comment in post.comments]

    disabled = False
    if session.get('username') is None:
        disabled = True
    
    return render_template('view_single_forum_post.html', post=post, forum_active=True, poster_username = poster_username, 
                           comment_usernames=comment_usernames, disabled=disabled)


@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    username = session.get('username')
    #abort with 401 if not logged in
    if username is None:
        abort(401)
    else:
        post = Post.query.get_or_404(post_id)
        post_author_id = post.author_id
        current_user_id = repository_singleton.get_user_by_username(username).user_id

        #abort with 403 if the currently logged in user isn't the post's author
        if post_author_id != current_user_id:
            abort(403)
        else:
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('view_forum_posts'))


@app.route('/delete_comment/<int:post_id>/<int:comment_id>', methods=['POST'])
def delete_comment(post_id, comment_id):
    username = session.get('username')
    if username is None:
        abort(401)
    else:
        comment = Comment.query.get_or_404(comment_id)
        comment_author_id = comment.author_id
        current_user_id = repository_singleton.get_user_by_username(username).user_id
        if comment_author_id != current_user_id:
            abort(403)
        else:
            db.session.delete(comment)
            db.session.commit()
            return redirect(url_for('view_single_forum_post', post_id=post_id))



@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_forum_post(post_id):
    disabled = False
    username = session.get('username')
    if username is None:
        disabled = True
    if username is None:
        abort(401) 
    post = Post.query.get_or_404(post_id)
    post_author_id = post.author_id
    current_user_id=repository_singleton.get_user_by_username(username).user_id
    if post_author_id != current_user_id:
        abort(403)
    else:
        if request.method == 'POST':
            new_subject = request.form['subject']
            new_body = request.form['body']
            new_course_id = request.form['course_id']
            if new_subject is None or new_body is None or new_course_id is None:
                abort(400)
            if repository_singleton.get_course_by_id(new_course_id) is None:
                abort(400)
            post.subject = new_subject
            post.body = new_body
            post.course_id = new_course_id
            db.session.commit()
            return redirect(url_for('view_forum_posts'))

        return render_template('edit_forum_post.html', post=post, courses=Course.query.all(), forum_active=True, disabled=disabled)

@app.route('/create_forum_comment/<int:post_id>', methods=['POST'])
def create_forum_comment(post_id):
    
    disabled = False
    if session.get('username') is None:
        disabled = True

    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        body = request.form['body']
        if body is None:
            abort(400)
        username = session.get('username')
        if username is None:
            abort(401)
        else:
            author_id = repository_singleton.get_user_by_username(username).user_id

    
        comment = Comment(body=body, post=post, author_id=author_id)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('view_single_forum_post', post_id=post_id, disabled=disabled))

@app.route('/edit_comment/<int:post_id>/<int:comment_id>', methods=['GET', 'POST'])
def edit_forum_comment(post_id, comment_id):
    disabled = False
    username = session.get('username')
    if username is None:
        disabled = True
    if username is None:
        abort(401) 
    comment = Comment.query.get_or_404(comment_id)
    comment_author_id = comment.author_id
    current_user_id = repository_singleton.get_user_by_username(username).user_id
    if comment_author_id != current_user_id:
        abort(403)
    else:
        if request.method == 'POST':
            new_body = request.form['body']
            if new_body is None:
                abort(400)
            comment.body = request.form['body']
            db.session.commit()
            return redirect(url_for('view_single_forum_post', post_id=post_id))

        return render_template('edit_forum_comment.html', comment=comment, post_id=post_id, forum_active=True, disabled=disabled)

@app.route('/login_signup')
def login_signup():
    return render_template('login_signup.html', login_active=True)

@app.route('/process_form', methods=['POST'])
def process_form():
    username = request.form.get('username')
    hashed_password = request.form.get('hashed_password')
    email=request.form.get('email')
    action = request.form.get('action')
    
    if not username or not hashed_password:
        flash('Please provide both username and password', 'error')
        return redirect('/login_signup')

    if action == 'Sign Up':
        bcrypt_password = bcrypt.generate_password_hash(hashed_password).decode()
        try:
            new_user = AppUser(username=username, hashed_password=bcrypt_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash('Account created successfully', 'success')
            return redirect('/user_profile')  # Redirect to user_profile after successful signup
        except IntegrityError:
            db.session.rollback()
            flash('Username already exists', 'error')
            return redirect('/login_signup')
    elif action == 'Login':
        try:
            existing_user = AppUser.query.filter_by(username=username).first()
            if not existing_user or hashed_password is None or not bcrypt.check_password_hash(existing_user.hashed_password, hashed_password):
                flash('Incorrect username or password', 'error')
                return redirect('/login_signup')
            session['username'] = username
            return redirect('/user_profile')
        except Exception as e:
            app.logger.error(f"Error during login: {str(e)}")
            flash('An error occurred during login', 'error')
            return redirect('/login_signup')
    else:
        return 'Invalid action'

@app.route('/user_profile')
def userprofile():
    username = session.get('username')
    if username is None:
        # Redirect to login page or handle unauthorized access
        return redirect('/login_signup')     
    return render_template('user_profile.html', username=username, user_active=True)

@app.route('/update_profile', methods=['PUT','POST'])
def update_profile():
    if request.method == 'POST':
        
        username = request.form.get('username')
        email = request.form.get('email')
        hashed_password = request.form.get('hashed_password')
        new_password = request.form.get('newPassword')
        return render_template('user_profile', username=username, email=email, messages=['Profile updated successfully!'])
    elif request.method == 'PUT':
        # Handle PUT request logic
        # For example, you can access form data using request.form
        username = request.form.get('username')
        hashed_password = request.form.get('hashed_password')
        newPassword = request.form.get('newPassword')
        email = request.form.get('email')

        return render_template('user_profile.html', username=username, email=email, messages=['Profile updated successfully!'])

    else:
        # Handle other HTTP methods if necessary
        return 'Method not allowed', 405
        # try:
        #     data = request.json  # Access JSON data from the request body
            
        #     # Extract relevant fields from the JSON data
        #     new_password = data.get('newPassword')
        #     username = data.get('username')
        #     email = data.get('email')
        #     hashed_password = data.get('hashed_password')
        # except Exception as e:
        #     # Log the exception traceback for debugging
        #     traceback.print_exc()

        #     # Return an error response
        #     error_response_data = {
        #         'message': 'Internal Server Error',
        #         'status': 'error'
        #     }

        #     error_response = app.response_class(
        #         response=json.dumps(error_response_data),
        #         status=500,
        #         mimetype='application/json'
        #     )

        #     return error_response
    # new_password = request.form.get('newPassword')
    # user.hashed_password = bcrypt.generate_password_hash(new_password).decode()
    # username = request.form.get('username')
    # email = request.form.get('email')
    # hashed_password = request.form.get('hashed_password')
    # new_password = request.form.get('newPassword')
    # user = AppUser.query.filter_by(username=username).first()

    # if not user or not bcrypt.check_password_hash(user.hashed_password, hashed_password):
    #     flash('Authentication failed. Please enter your current password correctly.', 'error')
    #     return redirect('/user_profile')

    # if new_password:
    #     user.hashed_password = bcrypt.generate_password_hash(new_password).decode()

    # user.email=email
    
    # try:
    #     db.session.commit()
    #     flash('Profile updated successfully', 'success')
    #     return redirect('/user_profile')
    # except IntegrityError:
    #     db.session.rollback()
    #     flash('Username already exists. Please choose another one.', 'error')
    # return redirect('/user_profile')
    

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect('/login_signup')

@app.route('/delete_user', methods=['GET','POST'])
def delete_user():
    if request.method == 'POST':
        username=session.get('username')
        try: 
            user_delete=AppUser.query.filter_by(username=username).first()
            db.session.delete(user_delete)
            db.session.commit()
            
            session.clear()
            
            flash('Your account has been deleted successfully.', 'success')
            return redirect('/login_signup')
        except IntegrityError:
            db.session.rollback()
            flash('Error deleting account failed. Please try again','error')
    return render_template('/index.html')


@app.get('/submit_rating')
def get_rating_form():
    disabled = False
    if session.get('username') is None:
        disabled = True
    courses = repository_singleton.get_all_courses()
    return render_template('submit_rating.html', rating_active=True, courses=courses, disabled=disabled)

@app.post('/submit_rating')
def submit_rating():
    # session checking
    username = session.get('username')
    if username is None:
        abort(401)
    else:
        author_id = repository_singleton.get_user_by_username(username).user_id
    
    # form stuff
    course_id = request.form.get('course')
    instructor = request.form.get('instructor')
    quality = request.form.get('quality')
    difficulty = request.form.get('difficulty')
    
    # input validation
    if course_id is None or instructor is None or quality is None or difficulty is None:
        abort(400)
    if repository_singleton.get_course_by_id(course_id) is None:
        abort(400)
    if int(quality) < 0 or int(quality) > 5 or int(difficulty) < 0 or int(difficulty) > 5:
        abort(400)
    
    grade = request.form.get('grade')
    if grade == 'none':
        grade = None
    if grade not in [None, 'A', 'B', 'C', 'D', 'F']:
        abort(400)
    description = request.form.get('description')
    if not description:
        description = None
    
    repository_singleton.create_rating(course_id=course_id, author_id=author_id, instructor=instructor, quality=quality, difficulty=difficulty, grade=grade, description=description)
    
    return redirect(f'/view_ratings/{course_id}')

@app.get('/view_ratings/<int:course_id>')
def view_ratings(course_id):
    course = repository_singleton.get_course_by_id(course_id)
    if course is None:
        abort(400) # invalid course_id
        
    ratings = repository_singleton.get_ratings_by_course(course_id)
    
    if ratings:
        qualities = [rating.quality for rating in ratings]
        avg_quality = round(sum(qualities) / len(qualities), 2)
        difficulties = [rating.difficulty for rating in ratings]
        avg_difficulty = round(sum(difficulties) / len(difficulties), 2)
    else:
        avg_quality = 'N/A'
        avg_difficulty = 'N/A'
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
    all_courses = repository_singleton.get_all_courses()

    majors_set = set()
    for course in all_courses:
        if course.major not in majors_set:
            majors_set.add(course.major)
    
    return render_template('course_directory_search.html', majors_set=majors_set, course_active=True)

@app.post('/search') #handles submissions
def post_search():
    #Nick
    major_choice = request.form.get('major') #getting form data from course_directory_search.html
    quality_choice = request.form.get('quality') 
    difficulty_choice = request.form.get('difficulty') 
    credit_choice = request.form.get('credit')

    # query in string format, so that the information gained from the forms can be used in course_directory(), edit: had to change this line because of bug where pages past the first page were not being sorted properly
    # uses .join to concatenate the key value pairs seperated by the & symbol, stopping empty parameters from being appended to the url, using the if value part at the end, making sure the value part of the key-value relationship is not empty
    query_parameters = '&'.join([f'{key}={value}' for key, value in {'major': major_choice, 'quality': quality_choice, 'difficulty': difficulty_choice, 'credit': credit_choice}.items() if value]) 

    #redirects to /directory with the appropriate query parameters that contain the data from the forms 
    return redirect(f'/directory?{query_parameters}') 


@app.get('/directory')
def course_directory():

    #beginning of pagination implementation, resources that helped me: https://betterprogramming.pub/simple-flask-pagination-example-4190b12c2e2e, https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.Pagination
    page = request.args.get('page', 1, type=int) #default page number = 1
    rows_per_page = 7  # number of rows/courses per page

    # get query parameters from the URL
    major_choice = request.args.get('major')
    quality_choice = request.args.get('quality')
    difficulty_choice = request.args.get('difficulty')
    credit_choice = request.args.get('credit')

    # starting/base query, joinedload also loads related ratings, not neccessary but I think it helps reduce potential amount of queries made to the db
    # these resourced helped me understand joinedload better: https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload, https://stackoverflow.com/questions/56440296/how-does-the-sqlalchemy-loading-methods-work
    courses_query = Course.query.options(joinedload(Course.ratings))

    # filter result if major parameter was selected
    if major_choice:
        courses_query = courses_query.filter_by(major=major_choice)

    # filter result if credit hour parameter was selected
    if credit_choice:
        courses_query = courses_query.filter_by(credits=credit_choice)

    # subquery, query nested inside another query, to get average difficulty and quality for each course using sqlalchemy function for averaging
    # resources that helped me: https://blog.miguelgrinberg.com/post/nested-queries-with-sqlalchemy-orm, https://stackoverflow.com/questions/7143235/how-to-use-avg-and-sum-in-sqlalchemy-query, https://stackoverflow.com/questions/11830980/sqlalchemy-simple-example-of-sum-average-min-max
    subquery = (
        db.session.query(
            Rating.course_id,
            func.avg(Rating.difficulty).label('avg_difficulty'),
            func.avg(Rating.quality).label('avg_quality')
        )
        .group_by(Rating.course_id)
        .subquery()
    )

    # joining subquery with the base query on course_id
    filtered_courses_query = courses_query.outerjoin(subquery, Course.course_id == subquery.c.course_id)  #.c for column

    # filtered_courses initialization
    filtered_courses = None

    # filter result if course quality parameter was selected
    if quality_choice:
        if quality_choice == "Quality1Plus":
            filtered_courses_query = filtered_courses_query.filter(subquery.c.avg_quality >= 1.0) #include only the courses where the average quality is 1.0 or higher using subquery column for average from earlier 
        elif quality_choice == "Quality2Plus":
            filtered_courses_query = filtered_courses_query.filter(subquery.c.avg_quality >= 2.0)
        elif quality_choice == "Quality3Plus":
            filtered_courses_query = filtered_courses_query.filter(subquery.c.avg_quality >= 3.0)
        elif quality_choice == "Quality4Plus":
            filtered_courses_query = filtered_courses_query.filter(subquery.c.avg_quality >= 4.0)
        elif quality_choice == "Quality5Only":
            filtered_courses_query = filtered_courses_query.filter(subquery.c.avg_quality == 5.0)

    # filter result if course difficulty parameter was selected
    if difficulty_choice:
        if difficulty_choice == "Diff1Plus":
            filtered_courses_query = filtered_courses_query.filter(subquery.c.avg_difficulty >= 1.0) #include only the courses where the average difficulty is 1.0 or higher using subquery column from earlier 
        elif difficulty_choice == "Diff2Plus":
            filtered_courses_query = filtered_courses_query.filter(subquery.c.avg_difficulty >= 2.0)
        elif difficulty_choice == "Diff3Plus":
            filtered_courses_query = filtered_courses_query.filter(subquery.c.avg_difficulty >= 3.0)
        elif difficulty_choice == "Diff4Plus":
            filtered_courses_query = filtered_courses_query.filter(subquery.c.avg_difficulty >= 4.0)
        elif difficulty_choice == "Diff5Only":
            filtered_courses_query = filtered_courses_query.filter(subquery.c.avg_difficulty == 5.0)       

    #filtered query, modified to use paginate(), which limits the query based on the page and number of courses/rows per page, error_out returns an empty pagination object instead of an error if there is an invalid page number
    filtered_courses = filtered_courses_query.paginate(page=page, per_page=rows_per_page, error_out=False)

    # loop for calculating average quality and difficulty for each course
    for course in filtered_courses:
        course.avg_quality = course.avg_difficulty = None
        for rating in course.ratings: #loop through each rating for the course
            if course.avg_quality is None:
                course.avg_quality = 0
            if course.avg_difficulty is None:
                course.avg_difficulty = 0
            course.avg_quality += rating.quality  #add up total for course
            course.avg_difficulty += rating.difficulty
        if course.avg_quality is not None:
            course.avg_quality /= len(course.ratings) #calculate average by dividing by amount of ratings
        if course.avg_difficulty is not None:
            course.avg_difficulty /= len(course.ratings) #calculate average by dividing by amount of ratings

    return render_template('course_directory.html', major_choice=major_choice, all_courses=filtered_courses, course_active=True)