from flask import Flask, render_template, request, make_response, session
import os

STATIC_FOLDER = 'templates/assets'
app=Flask(__name__, static_folder=STATIC_FOLDER) #initiating flask object

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.form['file']
        print(file)
        return render_template('index.html')
    elif request.method == 'GET':
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
