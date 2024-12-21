"""
Contains functions for making URL requests using requests library.
"""

import logging
import requests


def make_request(url: str, headers: dict = {}) -> requests.request:
    """
    Use requests library to make a url request and return response.

    Note: does not fail on error, caller must handle response content.

    Args:
        url (str): url to make request to.
        headers (dict, optional): headers for request.

    Returns:
        requests.request object.
    """
    request = requests.get(
        url,
        headers=headers
    )

    if request.status_code != 200:
        logging.warning("Could not resolve request to '%s'.", url)

    return request
