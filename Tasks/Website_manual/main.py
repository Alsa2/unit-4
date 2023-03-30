from flask import Flask, render_template, request, redirect, url_for, flash
import os

STATIC_FOLDER = 'templates/assets'
secret_key = os.urandom(24)
app=Flask(__name__, static_folder=STATIC_FOLDER) #initiating flask object

app.secret_key = secret_key

@app.route('/', methods=['GET'])
def index():
        return render_template('about.html')

@app.route("/post", methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        password = request.form['password']
        # check if password is secure
        #number 
        message = 'Password should have at least : '
        if not any(char.isdigit() for char in password):
            message += '1 number, '
        #uppercase
        if not any(char.isupper() for char in password):
            message += '1 uppercase letter, '
        #lowercase
        if not any(char.islower() for char in password):
            message += '1 lowercase letter, '
        #special character
        special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '|', ':', ';', '<', '>', '?', '/', '.']
        if not any(char in special_characters for char in password):
            message += '1 special character, '
        #length
        if len(password) < 8:
            message += '8 characters'
        #if last caracter is coma remove it
        if message[-2] == ',':
            message = message[:-2]
        if message != 'Password should have at least : ':
            flash(message)
            return render_template('request.html', result = message)
        else:
            return render_template('request.html', result = "Password is secure!")

    elif request.method == 'GET':
        initial_currency = request.args.get('from')
        final_currency = request.args.get('to')
        amout = request.args.get('amount')
        #if amount is not a number
        if initial_currency == None or final_currency == None or amout == None:
            flash("Please fill all the fields!")
            return render_template('request.html', result = "Please fill all the fields!")
        else:
            try:
                float(amout)
            except ValueError:
                flash("Please enter a number!")
                return render_template('request.html', result = "Please enter a number!")
            amout = float(amout)*1.2
        return render_template('request.html', result = amout)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
