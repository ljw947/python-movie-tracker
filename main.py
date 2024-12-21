#!/usr/bin/python3

"""
Main application body.
"""


import json
import logging
import sys

import movie_tracker


def main():
    """
    Load in cinema website info and make requests as needed.
    """
    cinemas = {}

    with open("cinemas.json") as cinema_list:
        cinemas = json.load(cinema_list)

    movies = movie_tracker.get_movies(cinemas["palace"]["movies"])

    if len(movies) == 0:
        logging.error("No movies found.")
        sys.exit(1)

    print(movies)

    sessions = movie_tracker.get_sessions(cinemas["palace"]["sessions"], "2024-12-21")

    print(sessions)


if __name__ == "__main__":
    main()
