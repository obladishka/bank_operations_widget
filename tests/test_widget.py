import pytest

from src.widget import mask_account_card


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
