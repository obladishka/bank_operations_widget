def get_mask_card_number(card_number: str | int, slots: int = 4) -> str:
    """Function that masks card number."""
    if card_number:

        if len(str(card_number)) < 12 or len(str(card_number)) > 19:
            raise ValueError("Card number should be between 12 and 19 digits")
        else:
            mask_card_number = (
                str(card_number)[:6]
                + "".join(["*" for i in range(len(str(card_number)) - 10)])
                + str(card_number)[-4:]
            )

            if len(str(card_number)) not in [14, 15]:
                return " ".join([mask_card_number[i : i + slots] for i in range(0, len(mask_card_number), slots)])
            else:
                return " ".join([mask_card_number[:4], mask_card_number[4:10], mask_card_number[10:]])

    else:
        return "Card number can't be empty"


def get_mask_account(account: int | str) -> str:
    """Function that masks account number."""
    if account:
        if len(str(account)) < 6 or len(str(account)) > 22:
            raise ValueError("Account should be between 6 and 22 digits")
        else:
            return "**" + str(account)[-4:]
    else:
        return "Account number can't be empty"
