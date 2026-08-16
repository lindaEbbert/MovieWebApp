# MovieWebApp

A small Flask web application for managing personal favourite-movie lists.
Users register with a name, pick their profile, and build a movie collection —
title, year, director and poster are fetched automatically from the
[OMDb API](https://www.omdbapi.com/).

Built as a portfolio project: the command-line movie app from an earlier module,
rebuilt as a dynamic web application with Flask, SQLAlchemy ORM and Jinja2 templates.

## Features

- **User management** — create users and select one from the start page
- **Movie management** — add, rename and delete movies per user
- **Automatic movie data** — year, director and poster come from OMDb; only the
  title is typed in
- **Optional year filter** — disambiguates remakes and titles that exist more than once
- **Per-user collections** — the same movie can appear in several users' lists
- **Error handling** — custom 404 and 500 pages, guarded database writes,
  graceful handling of unknown titles and network failures

## Tech stack

| Layer | Used |
|---|---|
| Language | Python 3.14 |
| Web framework | Flask 3.1 |
| ORM | Flask-SQLAlchemy 3.1 / SQLAlchemy 2.0 |
| Database | SQLite |
| Templating | Jinja2 |
| External API | OMDb |
| Styling | Plain CSS (no framework) |

## Project structure

```
MovieWebApp/
├── app.py              # Flask application, routes and error handlers
├── models.py           # SQLAlchemy models: User, Movie
├── data_manager.py     # DataManager class, all CRUD operations
├── omdb_api.py         # OMDb request and response normalisation
├── requirements.txt
├── .env.example        # template for the required environment variable
├── data/               # holds movies.db, created on first run
├── static/
│   └── style.css
└── templates/
    ├── base.html       # shared layout: header, content block, footer
    ├── index.html      # user list and "add user" form
    ├── movies.html     # movie cards and "add movie" form
    ├── 404.html
    └── 500.html
```

The application is deliberately split into three layers: `app.py` handles HTTP
concerns only, `DataManager` is the single place that talks to the database, and
`omdb_api.py` isolates the external API. No route touches `db.session` directly.

## Getting started

### Prerequisites

- Python 3.11 or newer
- A free OMDb API key — request one at
  [omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)
  and activate it via the link in the confirmation email

### Installation

```bash
git clone https://github.com/lindaEbbert/MovieWebApp.git
cd MovieWebApp
python -m venv .venv
```

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and insert your OMDb key:

```
OMDB_API_KEY=your_key_here
```

The `.env` file is git-ignored and never committed.

### Run

Start the development server:

```bash
python app.py
```

The application is available at http://localhost:5000. The SQLite database
`data/movies.db` and all tables are created automatically on first start.

## Routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | List all users, form for creating a new one |
| POST | `/users` | Create a user |
| GET | `/users/<user_id>/movies` | Show a user's movie list |
| POST | `/users/<user_id>/movies` | Add a movie via OMDb lookup |
| POST | `/users/<user_id>/movies/<movie_id>/update` | Rename a movie |
| POST | `/users/<user_id>/movies/<movie_id>/delete` | Delete a movie |

All state-changing routes use POST and answer with a redirect, so reloading the
page never repeats an action.

## Data model

**User** — `id`, `name` (unique)
**Movie** — `id`, `name`, `director`, `year`, `poster_url`, `user_id`

One user has many movies (1:n). Movies are deleted along with their user via
`cascade="all, delete-orphan"`. The movie title is intentionally **not** unique:
two users may keep the same film, each as their own row.

`director`, `year` and `poster_url` are nullable because OMDb returns `"N/A"`
for these fields on some entries.

## Notes

- `db.create_all()` only creates missing tables. After changing a model, delete
  `data/movies.db` and restart — the project has no migrations.
- OMDb's free tier allows 1000 requests per day.
- Unknown titles and network errors return `None` from `fetch_movie()` and leave
  the user on the movie list instead of raising an error.
