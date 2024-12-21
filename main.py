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

    locations = movie_tracker.get_locations(cinemas["palace"]["url"] + cinemas["palace"]["locations"])

    print(locations)

    movies = movie_tracker.get_movies(cinemas["palace"]["url"] + cinemas["palace"]["movies"] + "locality=brisbane")

    if len(movies) == 0:
        logging.error("No movies found.")
        sys.exit(1)

    print(movies)

    todays_date = "2024-12-22"
    sessions = movie_tracker.get_sessions(cinemas["palace"]["url"] + cinemas["palace"]["sessions"], todays_date)

    for session in sessions.values():
        for timeslot in session["sessions"]:
            if todays_date in timeslot:
                print(f"{session['title']} {timeslot}")


if __name__ == "__main__":
    main()
