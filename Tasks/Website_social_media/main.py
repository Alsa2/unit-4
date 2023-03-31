from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from db_handler import DBHandler
import dotenv
from jose import jwt
import datetime

STATIC_FOLDER = 'templates/assets'


app=Flask(__name__, static_folder=STATIC_FOLDER) #initiating flask object

dotenv.load_dotenv()
token_encryption_key = os.getenv('TOKEN_ENCRYPTION_KEY')

secret_key = os.urandom(24)
app.secret_key = secret_key


def create_token(username, token_duration): #token = encoded(username, datetime) token_duration in minutes
    token  = jwt.encode({'username': username, 'datetime': datetime.datetime.now() + datetime.timedelta(minutes=token_duration)}, token_encryption_key, algorithm='HS256')

def check_token(token): #check if token is valid and not expired
    try:
        decoded_token = jwt.decode(token, token_encryption_key, algorithms=['HS256'])
        if decoded_token['datetime'] < datetime.datetime.now():
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
        username = request.form.get['username']
        password = request.form.get['password']
        db = DBHandler()
        if db.login(username, password):
            token = create_token(username, 60)
            session['token'] = token
            return redirect(url_for('index'))
        else:
            flash('Wrong username or password')
            return redirect(url_for('login'))


