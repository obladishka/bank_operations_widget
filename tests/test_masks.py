import pytest

from src.masks import get_mask_card_number


def test_get_mask_card_number() -> None:
    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_get_mask_card_number_no_number() -> None:
    assert get_mask_card_number("") == "Card number can't be empty"


@pytest.mark.parametrize("card_number", [40128888188, 70007922896063610120])
def test_get_mask_card_number_wrong_number(card_number: int) -> None:
    with pytest.raises(ValueError, match="Card number should be between 12 and 19 digits"):
        get_mask_card_number(card_number)


@pytest.mark.parametrize(
    "card_number, expected",
    [
        (401288881888, "4012 88** 1888"),
        (4012888818888, "4012 88** *888 8"),
        (37598765432100, "3759 87**** 2100"),
        (375987654321001, "3759 87**** *1001"),
        (70007922896063610, "7000 79** **** *361 0"),
        (700079228960636101, "7000 79** **** **61 01"),
        (7000792289606361012, "7000 79** **** ***1 012"),
    ],
)
def test_get_mask_card_number_nonstandard_number(card_number: int, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected
