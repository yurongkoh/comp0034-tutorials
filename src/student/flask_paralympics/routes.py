from flask import Blueprint, render_template

# Define a Blueprint named 'main' for the main routes
main = Blueprint('main', __name__)

# Define a route for the main page
@main.route('/')

# Define a function called index that returns a simple message
def index():
    # return f"Hello!"
    return render_template('index.html')
