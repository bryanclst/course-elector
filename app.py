from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')

@app.get('/')
def index():
    return render_template('index.html')

@app.route('/login_signup')
def login_signup():
    return render_template('login_signup.html')

@app.route('/userprofile')
def userprofile():
    return render_template('userprofile.html')

if __name__ == '__main__':
    app.run(debug=True)