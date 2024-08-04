import pytest

from src.processing import analyze_categories, filter_by_state, search_by_srt, sort_by_date


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            None,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "20190703"},
                {"id": 939719571, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "20190703"},
                {"id": 939719571, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 615064591, "state": "CANCELED"},
            ],
        ),
    ],
)
def test_filter_by_state(
    operations_data: list[dict[str, str | int]], state: None | str, expected: list[dict[str, str | int]]
) -> None:
    """Tests filtering function with different states transmitted."""
    if state is None:
        filter_by_state(operations_data) == expected
    else:
        assert filter_by_state(operations_data, state) == expected


def test_filter_by_state_wrong_state(operations_data: list[dict[str, str | int]]) -> None:
    """Tests filtering function with wrong state."""
    assert filter_by_state(operations_data, state="PROCESSED") == "State is invalid"


def test_filter_by_state_no_data() -> None:
    """Tests filtering function with no data about transactions."""
    assert filter_by_state([]) == []


@pytest.mark.parametrize(
    "parameter, expected",
    [
        (
            False,
            [
                {"id": 615064591, "date": "2017-10-14T08:21:33.419441"},
                {"id": 939719571, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "20190703"},
            ],
        ),
        (
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "20190703"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719571, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 615064591, "date": "2017-10-14T08:21:33.419441"},
            ],
        ),
        (
            None,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "20190703"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719571, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 615064591, "date": "2017-10-14T08:21:33.419441"},
            ],
        ),
    ],
)
def test_sort_by_date(
    operations_data: list[dict[str, str | int]], parameter: bool, expected: list[dict[str, str | int]]
) -> None:
    """Tests sorting function with different transmitted parameters."""
    if parameter is None:
        sort_by_date(operations_data) == expected
    else:
        assert sort_by_date(operations_data, parameter) == expected


def test_sort_by_date_no_data() -> None:
    """Tests sorting function with no data about transactions."""
    assert sort_by_date([]) == []


@pytest.mark.parametrize(
    "search_str, transaction_index, number_of_transactions",
    [
        ("Перевод", 0, 5),
        ("Переводить", 0, 5),
        ("Перевести", 0, 5),
        ("перев", 0, 5),
        ("карта", 3, 1),
        ("открыть", 5, 1),
        ("открывать", 5, 1),
        ("Орг", 0, 2),
        ("со счета", 1, 2),
    ],
)
def test_search_by_srt(transactions, search_str, transaction_index, number_of_transactions):
    """Tests search_by_srt function with different strings for searching."""
    assert search_by_srt(transactions, search_str)[0] == transactions[transaction_index]
    assert len(search_by_srt(transactions, search_str)) == number_of_transactions


def test_search_by_srt_no_such_transactions(transactions):
    """Tests search_by_srt function when no transaction is found."""
    assert search_by_srt(transactions, "not existing word in description") == []


def test_search_by_srt_no_description():
    """Tests search_by_srt function when transaction has no description."""
    data = [
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]
    assert search_by_srt(data, "Перевод организации") == []


def test_analyze_categories(transactions):
    """Tests normal work of analyze_categories function."""
    categories_list = [
        "Перевод со счета на счет",
        "Перевод организации",
        "Перевод с карты на карту",
        "Открытие вклада",
    ]
    assert analyze_categories(transactions, categories_list) == {
        "Перевод со счета на счет": 2,
        "Перевод организации": 2,
        "Перевод с карты на карту": 1,
        "Открытие вклада": 1,
    }


def test_analyze_categories_no_such_category(transactions):
    """Tests analyze_categories function when category is not found."""
    assert analyze_categories(transactions, ["Not existing category"]) == {"Not existing category": 0}


def test_analyze_categories_no_descriptions():
    """Tests analyze_categories function when transaction has no description."""
    data = [
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]
    assert analyze_categories(data, ["Перевод организации", "Перевод с карты на карту"]) == {
        "Перевод организации": 0,
        "Перевод с карты на карту": 0,
    }
