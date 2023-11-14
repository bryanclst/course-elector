from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('homepage.html')

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