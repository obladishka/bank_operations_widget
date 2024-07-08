from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_info: str) -> str:
    """Function that masks input data accordingly."""
    info_list: list[str] = account_card_info.split()

    if not info_list[-1].isdigit() and info_list[0].lower() == "счет":
        return "Account number can't be empty"
    elif not info_list[-1].isdigit():
        return "Card number can't be empty"
    elif not info_list[0].isalpha():
        return "Type (account or card) can't be empty"
    else:

        if info_list[0].lower() == "счет":
            return " ".join(info_list[:-1]) + " " + get_mask_account(info_list[-1])
        elif len(info_list) > 3:
            card_number = [i for i in info_list if i.isdigit()]
            card_name = [i for i in info_list if i.isalpha()]
            return " ".join(card_name) + " " + get_mask_card_number("".join(card_number))
        else:
            return " ".join(info_list[:-1]) + " " + get_mask_card_number(info_list[-1])


def get_date(my_date: str) -> str:
    """Function for date formating."""
    if my_date:
        try:
            formated_date = str(datetime.fromisoformat(my_date))[:10].split("-")
        except ValueError:
            raise ValueError("Date should be in format YYYY-MM-DD")
        else:
            if datetime.fromisoformat(my_date).year < 1900 or datetime.fromisoformat(my_date).year > 2100:
                return "Date should be between 1900 and 2100 year"
            return ".".join(formated_date[::-1])
    return "Date can't be empty"
