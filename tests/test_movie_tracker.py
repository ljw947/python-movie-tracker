"""
Contains tests for movie_tracker module.
"""

# to monkeypatch
import requests

import json
import logging

import movie_tracker

GOOD_JSON = """
[
    {"movieId": "abc123", "title": "My Fake Title"},
    {"movieId": "123abc", "title": "My Fake Movie"}
]
"""


class MockRequests():
    """Create a mock requests object."""
    def __init__(self, json_return_type: str = None, status_code: int = 200):
        self.json_return_type = json_return_type
        self.status_code = status_code

    def status_code(self):
        return self.status_code

    def json(self):
        if self.json_return_type == "raise-error":
            raise json.decoder.JSONDecodeError("Expecting value", "doc", 0)
        elif self.json_return_type == "malformed-json":
            return {"bad_key": "bad_response"}
        elif self.json_return_type == "bad-json-key":
            return '''{"bad_key": {"bad_response": "bad_value"}}'''
        else:
            return json.loads(GOOD_JSON)


class TestGetMovies:
    """Groups tests for get_movies function."""
    def test_get_movies_bad_status_code(self, monkeypatch, caplog):
        def mock_get(*args, **kwargs):
            return MockRequests(json_return_type="raise-error", status_code=404)

        with caplog.at_level(logging.ERROR):
            monkeypatch.setattr(requests, "get", mock_get)
            movie_tracker.get_movies("")
        assert "Received no JSON response from request." in caplog.text

    def test_get_movies_no_json_response(self, monkeypatch, caplog):
        def mock_get(*args, **kwargs):
            return MockRequests(json_return_type="raise-error")

        with caplog.at_level(logging.ERROR):
            monkeypatch.setattr(requests, "get", mock_get)
            movie_tracker.get_movies("")
        assert "Received no JSON response from request." in caplog.text

    def test_get_movies_malformed_json_response(self, monkeypatch, caplog):
        def mock_get(*args, **kwargs):
            return MockRequests(json_return_type="malformed-json")

        with caplog.at_level(logging.ERROR):
            monkeypatch.setattr(requests, "get", mock_get)
            movie_tracker.get_movies("")
        assert "Recieved malformed JSON, not proceeding." in caplog.text

    def test_get_movies_bad_json_key_in_response(self, monkeypatch, caplog):
        def mock_get(*args, **kwargs):
            return MockRequests(json_return_type="bad-json-key")

        with caplog.at_level(logging.ERROR):
            monkeypatch.setattr(requests, "get", mock_get)
            movie_tracker.get_movies("")
        assert "Recieved malformed JSON, not proceeding." in caplog.text

    def test_get_movies_good_json_response(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockRequests()

        monkeypatch.setattr(requests, "get", mock_get)
        result = movie_tracker.get_movies("")
        print(result)
        assert result[0] == {'movieId': 'abc123', 'title': 'My Fake Title'}
