def get_mask_card_number(card_number: str | int, slots: int = 4) -> str:
    """Function that masks card number."""
    mask_card_number = str(card_number)[:6] + "******" + str(card_number)[-4:]
    return " ".join([mask_card_number[i : i + slots] for i in range(0, len(mask_card_number), slots)])


def get_mask_account(account: int | str) -> str:
    """Function that masks account number."""
    return "**" + str(account)[-4:]
