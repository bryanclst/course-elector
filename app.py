from flask import Flask, render_template, redirect, request, abort

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('homepage.html') #changed from index.html to homepage.html as we do not have an index.html page

@app.get('/about')
def about_us():
    #Nick
    return render_template('about_us.html')

@app.get('/search')
def get_search():
    #Nick
    return render_template('course_directory_search.html')

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

    return render_template('course_directory.html', major_choice=major_choice) #would in theory be feeding in list of courses, just using major_choice for testing

