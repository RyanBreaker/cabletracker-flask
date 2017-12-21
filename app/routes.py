from flask import render_template
from app import app


@app.route('/')
def hello_world():
    user = {'username': 'Miguel'}
    return render_template('index.html', user=user)
