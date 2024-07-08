import pytest

from src.processing import filter_by_state, sort_by_date


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
    if state is None:
        filter_by_state(operations_data) == expected
    else:
        assert filter_by_state(operations_data, state) == expected


def test_filter_by_state_wrong_state(operations_data: list[dict[str, str | int]]) -> None:
    assert filter_by_state(operations_data, state="PROCESSED") == "State is invalid"


def test_filter_by_state_no_data() -> None:
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
    if parameter is None:
        sort_by_date(operations_data) == expected
    else:
        assert sort_by_date(operations_data, parameter) == expected


def test_sort_by_date_no_data() -> None:
    assert sort_by_date([]) == []
