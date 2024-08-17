from unittest import mock
from unittest.mock import patch

import requests

from src.external_api import get_exchange_rate


@patch("src.external_api.requests.get")
def test_get_exchange_rate(mock_get):
    """Tests normal work of get_exchange_rate function."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 25},
        "info": {"timestamp": 1722061984, "rate": 85.972867},
        "date": "2024-07-27",
        "result": 2149.321675,
    }
    result = get_exchange_rate(25, "USD")
    assert result == (True, 2149.32)


@patch("src.external_api.requests.get")
def test_get_exchange_rate_denied_access(mock_get):
    """Tests get_exchange_rate function with incorrect API_KEY."""
    mock_get.return_value.status_code = 401
    mock_get.return_value.reason = "Unauthorized"
    mock_get.return_value.json.return_value = {"message": "Invalid authentication credentials"}
    result = get_exchange_rate(25, "USD")
    assert result == (False, "Unauthorized")


def test_get_exchange_rate_request_error():
    """Tests get_exchange_rate function when request error occures."""
    with mock.patch("requests.get", side_effect=requests.exceptions.RequestException("Something went wrong")):
        result = get_exchange_rate(25, "USD")
    assert result == (False, "Something went wrong")
