import os

from flask import Flask, render_template, request, redirect, url_for

from models import db, User, Movie
from data_manager import DataManager

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route("/", methods=["GET"])
def index():
    """Render the index page."""
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user. If the name is empty,
    redirect to the index.
    """

    user_name = request.form.get("name","").strip()
    if not user_name:
        return redirect(url_for("index"))

    data_manager.create_user(user_name)
    return redirect(url_for("index"))


@app.route('/users/<int:user_id>/movies')
def get_movies(user_id):
    """Get movies for a user."""

    return f"Movies for user: {user_id}"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
