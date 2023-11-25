from flask import Flask, render_template, redirect, request, abort, url_for, session
from dotenv import load_dotenv
from models import db, User
from flask_bcrypt import Bcrypt
import os

load_dotenv()
app = Flask(__name__, static_url_path='/static')

env= os.getenv('ENVIRONMENT')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# TODO: DB connection
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=env=='local'

db.init_app(app)
bcrypt = Bcrypt(app)


#structures to hold posts and comments
class_list = [
    {"code": "ITCS 3155"},
    {"code": "JAPN 3202"}
]
posts = []
comments = {}

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/view_forum_posts')
def view_forum_posts():
    return render_template('view_forum_posts.html', posts=posts, forum_active = True)

@app.route('/create_forum_post', methods=['GET', 'POST'])
def create_forum_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        selected_code = request.form['code']
        posts.append({'title': title, 'content': content, 'code': selected_code})
        return redirect(url_for('view_forum_posts'))
    return render_template('create_forum_post.html', class_list=class_list, forum_active = True)


@app.route('/view_single_forum_post/<int:post_id>', methods=['GET', 'POST'])
def view_single_forum_post(post_id):
    if request.method == 'POST':
        comment = request.form['comment']
        if post_id not in comments:
            comments[post_id] = []
        comments[post_id].append(comment)
    post_data = posts[post_id] if post_id < len(posts) else None
    return render_template('view_single_forum_post.html', post=post_data, comments=comments.get(post_id, []), post_id=post_id, forum_active = True)


@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    if post_id < len(posts):
        del posts[post_id]
    return redirect(url_for('view_forum_posts'))

@app.route('/delete_comment/<int:post_id>/<int:comment_id>', methods=['POST'])
def delete_comment(post_id, comment_id):
    if post_id in comments and comment_id < len(comments[post_id]):
        del comments[post_id][comment_id]
    return redirect(url_for('view_single_forum_post', post_id=post_id))

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_forum_post(post_id):
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        if post_id < len(posts):
            posts[post_id]['title'] = new_title
            posts[post_id]['content'] = new_content
            return redirect(url_for('view_single_forum_post', post_id=post_id))
    post_data = posts[post_id] if post_id < len(posts) else None
    return render_template('edit_forum_post.html', post=post_data, post_id=post_id, forum_active = True)

@app.route('/edit_comment/<int:post_id>/<int:comment_id>', methods=['GET', 'POST'])
def edit_forum_comment(post_id, comment_id):
    if request.method == 'POST':
        new_comment = request.form['comment']
        if post_id in comments and comment_id < len(comments[post_id]):
            comments[post_id][comment_id] = new_comment
            return redirect(url_for('view_single_forum_post', post_id=post_id))
    post_data = posts[post_id] if post_id < len(posts) else None
    return render_template('edit_forum_comment.html', comment=comments[post_id][comment_id], post=post_data, post_id=post_id, comment_id=comment_id, forum_active = True)

@app.route('/login_signup')
def login_signup():
    return render_template('login_signup.html', login_active=True)

@app.post('/signup')
def signup():
    username=request.form.get('username')
    hashed_password=request.form.get('hashed_password')
    if not username or not hashed_password:
        abort (400)
    bcrypt_password=bycrypt.generate_password_has(hashed_password,12).decode()
    new_user = User(username,bcrypt_password)
    db.session.add(new_user)
    db.session.commit()
    return redirect('login_signup.html')

@app.post('/login')
def login():
    username=request.form.get('username')
    hashed_password=request.form.get('hashed_password')
    if not username or not hashed_password:
        abort (400)
    existing_user = User.query.filter_by(username=username).first_or_404()
    if not existing_user:
        abort(401)
    if not bcrypt.check_password_hash(existing_user.password, hashed_password):
        abort(401)
    return redirect('/user_profile')


@app.route('/user_profile')
def userprofile():
    if 'username' not in session:
        abort(401)
    return render_template('user_profile.html', username=session['username'], user_active=True)

@app.get('/submit_rating')
def get_rating_form():
    return render_template('submit_rating.html', rating_active=True)

@app.post('/submit_rating')
def submit_rating():
    # do stuff with rating form
    return redirect('/view_ratings') # TODO change to append the id of the rating eventually

@app.get('/view_ratings') # TODO variable to access specific id
def view_ratings():
    return render_template('view_ratings.html', rating_active=True)

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


