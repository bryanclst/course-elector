from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')

@app.get('/')
def index():
    return render_template('index.html')

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
    return render_template('view_ratings.html', rating_active=True)

if __name__ == '__main__':
    app.run(debug=True)