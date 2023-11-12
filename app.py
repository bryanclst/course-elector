from flask import Flask, render_template

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('homepage.html')

@app.get('/submit_rating')
def get_rating_form():
    return render_template('submit_rating.html', rating_active=True)

@app.post('/submit_rating')
def submit_rating():
    return render_template('view_ratings.html', rating_active=True)