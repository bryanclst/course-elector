from flask import Flask, render_template, redirect, request, abort

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/submit_rating')
def get_rating_form():
    return render_template('submit_rating.html', rating_active=True)

@app.post('/submit_rating')
def submit_rating():
    return render_template('view_ratings.html', rating_active=True)

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



