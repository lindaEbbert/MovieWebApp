from sqlalchemy.exc import SQLAlchemyError
from models import db, User, Movie


class DataManager:
    """All data related operations."""

    def create_user(self, name: str) -> User:
        """Create a new user.

        :param name: User's name.
        :return: The created user object.
        """

        user = User(name=name)
        db.session.add(user)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        return user


    def get_users(self) -> list[User]:
        """Get all users ordered by name.

        :return: A list of user objects.
        """

        statement = db.select(User).order_by(User.name)
        return db.session.execute(statement).scalars().all()


    def get_movies(self, user_id: int) -> list[Movie]:
        """Get all movies from a user.

        :param user_id: User's ID.
        :return: A list of movie objects.
        """

        statement = db.select(Movie).where(Movie.user_id == user_id)
        return db.session.execute(statement).scalars().all()


    def get_user(self, user_id: int) -> User:
        """Get a user by ID."""

        return db.session.get(User, user_id)


    def add_movie(self, movie: Movie) -> None:
        """Add a movie to the database.

        :param movie: Movie object to add (must have user_id set).
        """

        db.session.add(movie)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e


    def update_movie(self, movie: Movie, new_title: str) -> Movie | None:
        """Update a movie title in the database.

        :param movie: Movie object to update.
        :param new_title: New title for the movie.
        :return: Updated movie object, or None if not found."""

        updated_movie = db.session.get(Movie, movie.id)
        if updated_movie is None:
            return None
        updated_movie.title = new_title
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        return updated_movie


    def delete_movie(self, movie_id: int):
        """Delete a movie from the database."""

        movie = db.session.get(Movie, movie_id)
        if not movie:
            return False

        db.session.delete(movie)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        return True