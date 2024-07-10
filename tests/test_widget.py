import pytest

from src.widget import get_date, mask_account_card


def test_mask_account_card() -> None:
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


@pytest.mark.parametrize(
    "account_card_number, expected",
    [
        ("Maestro 159683785199", "Maestro 1596 83** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Visa Classic 6831 9824 7673 7658 01", "Visa Classic 6831 98** **** **58 01"),
        ("MasterCard 375987654321001", "MasterCard 3759 87**** *1001"),
        ("Счет 646864", "Счет **6864"),
        ("Visa Platinum 8990 9221 1366 5229", "Visa Platinum 8990 92** **** 5229"),
    ],
)
def test_mask_account_card_nonstandard_number(account_card_number: str, expected: str) -> None:
    assert mask_account_card(account_card_number) == expected


def test_mask_account_card_no_number_or_type() -> None:
    assert mask_account_card("Счет") == "Account number can't be empty"
    assert mask_account_card("Visa Platinum") == "Card number can't be empty"
    assert mask_account_card("159683785199") == "Type (account or card) can't be empty"


@pytest.mark.parametrize(
    "account_card_number",
    [
        "Счет 73654",
        "Счет 73654108430135874305123",
        "Visa Platinum 40128888188",
        "MasterCard 70007922896063610120",
    ],
)
def test_mask_account_card_wrong_number(account_card_number: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(account_card_number)


def test_get_date() -> None:
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


@pytest.mark.parametrize(
    "my_date, expected",
    [
        ("20240311", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
        ("20050809T183142", "09.08.2005"),
        ("20050809T183142+03", "09.08.2005"),
        ("2005-08-09T18:31:42-03", "09.08.2005"),
        ("20050809T183142+0330", "09.08.2005"),
        ("2005-08-09T18:31:42-03:30", "09.08.2005"),
        ("2005-08-09T18:31:42.201", "09.08.2005"),
    ],
)
def test_get_date_different_formats(my_date: str, expected: str) -> None:
    assert get_date(my_date) == expected


def test_get_date_no_date() -> None:
    assert get_date("18990809T183142") == "Date should be between 1900 and 2100 year"
    assert get_date("21010809T183142") == "Date should be between 1900 and 2100 year"


def test_get_date_wrong_date() -> None:
    assert get_date("") == "Date can't be empty"


@pytest.mark.parametrize(
    "my_date",
    [
        "2019-07T18:35:29.512364",
        "2019.07T18:35:29.512364",
        "202403",
    ],
)
def test_get_date_wrong_date_format(my_date: str) -> None:
    with pytest.raises(ValueError, match="Date should be in format YYYY-MM-DD"):
        get_date(my_date)
