import os

from flask import abort, Flask, render_template, request, redirect, url_for

from models import db, Movie
from data_manager import DataManager
from omdb_api import fetch_movie

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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

    user_name = request.form.get("name", "").strip()
    if not user_name:
        return redirect(url_for("index"))

    data_manager.create_user(user_name)
    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def get_movies(user_id):
    """Get movies for a user."""

    user = data_manager.get_user(user_id)
    if not user:
        abort(404)

    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=movies, user=user)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    """Add a movie to a user's list."""

    title = request.form.get("name").strip()
    year = request.form.get("year")
    if not year:
        year = None
    else:
        try:
            year = int(year)
        except ValueError:
            year = None

    user = data_manager.get_user(user_id)
    if not user:
        abort(404)
    movie_details = fetch_movie(title, year)
    if not movie_details:
        return redirect(url_for("get_movies", user_id=user_id))
    movie = Movie(
        user_id=user_id,
        name=movie_details["name"],
        year=movie_details["year"],
        poster_url=movie_details["poster_url"],
        director=movie_details["director"],
    )
    data_manager.add_movie(movie)
    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_movie(user_id, movie_id):
    """Update a movie's title."""

    user = data_manager.get_user(user_id)
    if not user:
        abort(404)
    new_title = request.form.get("new_title").strip()
    if not new_title:
        return redirect(url_for("get_movies", user_id=user_id))

    updated_movie = data_manager.update_movie(movie_id, new_title)
    if not updated_movie:
        abort(404)
    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    """Delete a movie from a user's list."""

    user = data_manager.get_user(user_id)
    if not user:
        abort(404)

    is_deleted = data_manager.delete_movie(movie_id)
    if not is_deleted:
        abort(404)
    return redirect(url_for("get_movies", user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
