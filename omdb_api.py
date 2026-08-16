import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")


def format_response(data: dict) -> dict:
    """Format the response from OMDb API.
    This function removes unnecessary keys, renames keys,
    and saves "N/A" values as None.

    :param data: The response data from OMDb API.
    :return: A formatted dictionary that contains only
    name, year, director, and poster_url.
    """

    annotations = {"name": "Title",
                   "year": "Year",
                   "director": "Director",
                   "poster_url": "Poster"}

    formatted_response = {}
    for key, value in annotations.items():
        if key in ["director", "poster_url"]:
            if data[value] == "N/A":
                formatted_response[key] = None
            else:
                formatted_response[key] = data.get(value, None)
        elif key == "year":
            try:
                formatted_response[key] = int(data.get(value, None))
            except ValueError:
                formatted_response[key] = None
        else:
            formatted_response[key] = data.get(value)

    return formatted_response


def fetch_movie(title: str, year=None) -> dict | None:
    """Fetch movie details from OMDb API.

    :param title: The title of the movie to fetch.
    :param year: The year of the movie to fetch (optional).
    :return: A formatted dictionary containing only the necessary
    keys (name, year, director, poster_url).
    """

    url = f"https://www.omdbapi.com/"

    if not API_KEY:
        raise ValueError("API key is not set in environment variables.")
    params = {"apikey": API_KEY,
                  "t": title}
    if year:
        params["y"] = year

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching movie details: {e}")
        return None
    data = response.json()
    if data.get("Response") != "True":
        return None
    return format_response(data)
