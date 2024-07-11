import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency(transactions):
    usd_transactions = filter_by_currency(transactions, "USD")
    assert next(usd_transactions) == {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    assert next(usd_transactions) == {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    }
    rub_transactions = filter_by_currency(transactions, "RUB")
    assert next(rub_transactions) == {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    }


def test_filter_by_currency_no_transactions(transactions):
    assert filter_by_currency(transactions, "EUR") == "No transactions in such currency"
    assert filter_by_currency([], "USD") == "No transactions in such currency"


def test_filter_by_currency_no_currency():
    no_currency_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]
    assert filter_by_currency(no_currency_transactions, "USD") == "No transactions in such currency"


def test_transaction_descriptions(transactions):
    descriptions = transaction_descriptions(transactions)
    assert next(descriptions, "No more transactions") == "Перевод организации"
    assert next(descriptions, "No more transactions") == "Перевод со счета на счет"
    assert next(descriptions, "No more transactions") == "Перевод со счета на счет"
    assert next(descriptions, "No more transactions") == "Перевод с карты на карту"
    assert next(descriptions, "No more transactions") == "Перевод организации"
    assert next(descriptions, "No more transactions") == "Перевод организации"
    assert next(descriptions, "No more transactions") == "Operation description is not defined"
    assert next(descriptions, "No more transactions") == "No more transactions"


def test_transaction_descriptions_no_transactions():
    assert next(transaction_descriptions([])) == "No transactions found"


def test_transaction_descriptions_no_description():
    no_description_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]
    assert next(transaction_descriptions(no_description_transactions)) == "Operation description is not defined"
    assert next(transaction_descriptions(no_description_transactions)) == "Operation description is not defined"


def test_card_number_generator():
    card_number = card_number_generator(1, 5)
    assert next(card_number) == "0000 0000 0000 0001"
    assert next(card_number) == "0000 0000 0000 0002"
    assert next(card_number) == "0000 0000 0000 0003"
    assert next(card_number) == "0000 0000 0000 0004"
    assert next(card_number) == "0000 0000 0000 0005"


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (
            1000,
            1003,
            [
                "0000 0000 0000 1000",
                "0000 0000 0000 1001",
                "0000 0000 0000 1002",
                "0000 0000 0000 1003",
            ],
        ),
        (
            10000010,
            10000013,
            [
                "0000 0000 1000 0010",
                "0000 0000 1000 0011",
                "0000 0000 1000 0012",
                "0000 0000 1000 0013",
            ],
        ),
        (
            100000000100,
            100000000103,
            [
                "0000 1000 0000 0100",
                "0000 1000 0000 0101",
                "0000 1000 0000 0102",
                "0000 1000 0000 0103",
            ],
        ),
        (
            1000000000001000,
            1000000000001003,
            [
                "1000 0000 0000 1000",
                "1000 0000 0000 1001",
                "1000 0000 0000 1002",
                "1000 0000 0000 1003",
            ],
        ),
        (
            9999999999999996,
            9999999999999999,
            [
                "9999 9999 9999 9996",
                "9999 9999 9999 9997",
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
            ],
        ),
    ],
)
def test_card_number_generator_different_ranges(a, b, expected):
    result = list(card_number for card_number in card_number_generator(a, b))
    assert result == expected


def test_card_number_generator_extreme_numbers():
    assert next(card_number_generator(0, 1)) == "Range should be between 1 and 9999999999999999"
    assert next(card_number_generator(1, 10000000000000000)) == "Range should be between 1 and 9999999999999999"
    assert next(card_number_generator(1, 0)) == "Min range should be smaller than max range"
