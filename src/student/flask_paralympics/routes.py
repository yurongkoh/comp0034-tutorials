from flask import Blueprint, render_template, request
from student.flask_paralympics.db import get_db

# Define a Blueprint named 'main' for the main routes
main = Blueprint('main', __name__)

# Define a route for the main page
@main.route('/')
@main.route('/<name>')

# Define a function called index that returns a personalized message
def index(name=None):
    return render_template('index.html', name=name)

@main.route('/events')
def get_events():
    db = get_db()
    events = db.execute('SELECT * FROM Event').fetchall()
    events_text = [f'{event["year"]} {event["type"]} {event["start"]} {event["end"]}' for event in events]
    return events_text