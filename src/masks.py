import logging
import os

log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "masks.log")

logger = logging.getLogger("masks")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path, mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str | int, slots: int = 4) -> str:
    """Function that masks card number."""
    logger.info(f"Masking card {card_number}")
    if card_number:

        if len(str(card_number)) < 12 or len(str(card_number)) > 19:
            logger.critical(f"Wrong card number: {card_number}")
            raise ValueError("Card number should be between 12 and 19 digits")

        else:
            mask_card_number = (
                str(card_number)[:6]
                + "".join(["*" for i in range(len(str(card_number)) - 10)])
                + str(card_number)[-4:]
            )

            if len(str(card_number)) not in [14, 15]:
                logger.info(f"{len(mask_card_number)}-digit card masked successfully")
                return " ".join([mask_card_number[i : i + slots] for i in range(0, len(mask_card_number), slots)])
            else:
                logger.info(f"{len(mask_card_number)}-digit card masked successfully")
                return " ".join([mask_card_number[:4], mask_card_number[4:10], mask_card_number[10:]])

    else:
        logger.warning("No card number transmitted")
        return "Card number can't be empty"


def get_mask_account(account: int | str) -> str:
    """Function that masks account number."""
    logger.info(f"Masking account {account}")

    if account:
        if len(str(account)) < 6 or len(str(account)) > 22:
            logger.critical(f"Wrong account number: {account}")
            raise ValueError("Account should be between 6 and 22 digits")
        else:
            logger.info(f"{len(str(account))}-digit account masked successfully")
            return "**" + str(account)[-4:]
    else:
        logger.warning("No account number transmitted")
        return "Account number can't be empty"
