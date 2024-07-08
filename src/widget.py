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


def get_data(my_date: str) -> str:
    """Function for date formating."""
    formated_date: list[str] = my_date[:10].split("-")
    return ".".join(formated_date[::-1])
