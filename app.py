from flask import Flask, render_template, redirect, request, abort, url_for
from src.models import db, AppUser, Course, Rating, Post, Comment
from dotenv import load_dotenv
import os

from src.repositories.repository import repository_singleton

from sqlalchemy import func, cast, Float 
from sqlalchemy.orm import joinedload 
from flask_sqlalchemy import pagination #just added
load_dotenv()

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
db.init_app(app)

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

@app.route('/user_profile')
def userprofile():
    return render_template('user_profile.html', user_active=True)

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

    # query in string format, so that the information gained from the forms can be used in course_directory()
    query_parameters = f'major={major_choice}&quality={quality_choice}&difficulty={difficulty_choice}&credit={credit_choice}' 

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