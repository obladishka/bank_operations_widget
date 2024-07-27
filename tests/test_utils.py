import json
import os
import tempfile
from unittest.mock import patch

import pytest

from src.utils import get_operations_data, get_transaction_amount


def test_get_operations_data():
    """Tests normal work of get_operations_data function."""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")
    assert get_operations_data(file_path)[:2] == [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
    ]


def test_get_operations_data_no_such_file():
    """Tests get_operations_data function when a JSON-file does not exist."""
    file_name = "no_such_file.json"
    assert get_operations_data(file_name) == []


def test_get_operations_data_empty_file():
    """Tests get_operations_data function when a JSON-file is empty."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        file_path = tmp_file.name
    assert get_operations_data(file_path) == []


def test_get_operations_data_not_a_list():
    """Tests get_operations_data function when a JSON-file does not contain a list."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
        data = {
            "people": [
                {
                    "name": "John Smith",
                    "phone": "666-555-444",
                    "emails": ["johnsmith@home.com", "john.smith@work.com"],
                    "has_license": False,
                },
                {"name": "Jane Doe", "phone": "111-222-333", "emails": None, "has_license": True},
            ]
        }
        json.dump(data, tmp_file)
        file_path = tmp_file.name
    assert get_operations_data(file_path) == []


def test_get_transaction_amount(transactions):
    """Tests work of get_transaction_amount function with RUB transactions."""
    rub_transaction = transactions[2]
    assert get_transaction_amount(rub_transaction) == 43318.34


@patch("src.utils.get_exchange_rate")
def test_get_transaction_amount_non_ruble_transactions(mock_get_exchange_rate):
    """Tests successful conversion of USD transaction."""
    mock_get_exchange_rate.return_value = (True, 2149.32)
    usd_transaction = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "25", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    result = get_transaction_amount(usd_transaction)
    assert result == 2149.32


@pytest.mark.parametrize("return_status, return_result", [(False, "Unauthorized"), (False, "Something went wrong")])
@patch("src.utils.get_exchange_rate")
def test_get_transaction_amount_non_ruble_transactions_unsuccessful(
    mock_get_exchange_rate, return_status, return_result
):
    """Tests unsuccessful conversion of USD transaction."""
    mock_get_exchange_rate.return_value = (return_status, return_result)
    usd_transaction = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "25", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    result = get_transaction_amount(usd_transaction)
    assert result is None
