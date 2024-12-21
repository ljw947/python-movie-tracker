"""
Contains logic for tracking movies and sessions.
"""


import logging
import json

import requester


def get_json_response(endpoint: str) -> dict:
    """
    Get JSON response from requester.

    Args:
        endpoint (str): URL of cinema's web API to request data from.

    Returns:
        dict representing JSON response, no guarantee of keys etc.
    """
    json_response = {}

    response = requester.make_request(endpoint)

    try:
        json_response = response.json()
    except json.decoder.JSONDecodeError:
        logging.error("Received no JSON response from request.")
        return json_response

    return json_response


def get_movies(movie_list_api_endpoint: str) -> dict[str: str, str]:
    """
    Get full list of movies at cinema.

    Args:
        movie_list_api_endpoint (str): URL of cinema's web API to get list of movies from.

    Return:
        dict[str, str] with movieId as key; movieId and title as values.
    """
    movies = get_json_response(movie_list_api_endpoint)

    for movie in movies:
        try:
            movies[movie["movieId"]] = {"movieId": movie["movieId"], "title": movie["title"]}
        except KeyError as ex:
            logging.error("Unexpected key '%s' found in response, not proceeding.", ex.args[0])
            break
        except TypeError:
            logging.error("Recieved malformed JSON, not proceeding.")
            break

    return movies


def get_sessions(session_list_api_endpoint: str, date: str) -> dict[str: str, str, list[str]]:
    """
    Get full list of sessions at cinema.

    Args:
        session_list_api_endpoint (str): URL of cinema's web API to get list of sessions from.
        date (str): Date to query web API for sessions.

    Return
        dict[str: str, str, list[str]] with movieId as key; movieId, title and list of sessions times as values.
    """

    def update_sessions(sessions: dict, response: dict) -> None:
        """Inline function to mangle session response data into a format we need."""
        for movie in response["data"]:
            movie_sessions = []
            for session in movie["sessions"]:
                movie_sessions.append(session["date"])

            sessions.update({
                movie["movieId"]: {
                    "movieId": movie["movieId"],
                    "title": movie["title"],
                    "sessions": movie_sessions
                }
            })

    sessions = {}

    initial_session = get_json_response(
        session_list_api_endpoint + f"selectedDates={date}" + "&selectedCinemaIds=121" + "&page=1")

    update_sessions(sessions, initial_session)

    # we already have page 1
    for page_number in range(2, initial_session["totalPages"]):
        update_sessions(sessions, get_json_response(
            session_list_api_endpoint + f"selectedDates={date}" + "&selectedCinemaIds=121" + f"&page={page_number}"))

    return sessions
