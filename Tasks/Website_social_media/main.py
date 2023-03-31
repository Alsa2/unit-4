from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from db_handler import DatabaseHandler
#import dotenv
from jose import jwt
# add unix epoch time
from datetime import datetime

STATIC_FOLDER = 'templates/assets'


app=Flask(__name__, static_folder=STATIC_FOLDER) #initiating flask object

#dotenv.load_dotenv()
#token_encryption_key = os.getenv('TOKEN_ENCRYPTION_KEY')
token_encryption_key = 'secret'

secret_key = os.urandom(24)
app.secret_key = secret_key


def create_token(username, token_duration): #token = encoded(username, datetime) token_duration in minutes
    # Unix Epoch time
    unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    ttl = token_duration * 60 + unix_timestamp
    token  = jwt.encode({'username': username, 'datetime': unix_timestamp}, token_encryption_key, algorithm='HS256')

def check_token(token): #check if token is valid and not expired
    try:
        decoded_token = jwt.decode(token, token_encryption_key, algorithms=['HS256'])
        unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
        if decoded_token['datetime'] < unix_timestamp:
            return False
        else:
            return True
    except:
        return False



def login_required(f):
    def wrapper(*args, **kwargs):
        if 'token' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))

    return wrapper

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        db = DatabaseHandler()
        if db.login(username, password):
            token = create_token(username, 60)
            session['token'] = token
            db.close()
            return render_template('index.html', username=username)
        else:
            flash('Wrong username or password')
            return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        db = DatabaseHandler()
        if db.get_user_by_username(username) is None:
            db.add_user(username, password)
            db.close()
            return redirect('/login')
        else:
            flash('Username already exists')
            return redirect(url_for('register'))

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))

@app.route('/test')
def test():
    token = session['token']
    print(token)
    return token

if __name__ == '__main__':
    app.run(debug=True)

