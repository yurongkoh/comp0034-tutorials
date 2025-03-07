from flask import Blueprint, render_template, request

# Define a Blueprint named 'main' for the main routes
main = Blueprint('main', __name__)

# Define a route for the main page
@main.route('/')
@main.route('/<name>')

# Define a function called index that returns a personalized message
def index(name=None):
    return render_template('index.html', name=name)
