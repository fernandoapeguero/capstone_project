from models import app, db, Venue, Team, Events
from flask import jsonify
from auth import requires_auth


@app.route('/')
def index():

    return "This is the home"



if __name__ == "__main__":
    app.run()