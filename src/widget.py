from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_info: str) -> str:
    """Function that masks input data accordingly."""
    info_list: list[str] = account_card_info.split()

    if info_list[0].lower() == "счет":
        masked_info: str = get_mask_account(info_list[-1])
    else:
        masked_info = get_mask_card_number(info_list[-1])

    return " ".join(info_list[:-1]) + " " + masked_info


def get_data(my_date: str) -> str:
    """Function for date formating."""
    formated_date: list[str] = my_date[:10].split("-")
    return ".".join(formated_date[::-1])
