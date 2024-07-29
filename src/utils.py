import json
import logging
import os
from typing import Any

from src.external_api import get_exchange_rate

log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "utils.log")

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path, mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_operations_data(file_path: str) -> list[dict]:
    """Function that returns info about financial transactions from JSON-file."""
    try:
        logger.info(f"Trying to open a file {file_path}")
        with open(file_path, "r", encoding="utf-8") as data_file:

            try:
                logger.info("Trying to deserialize file data")
                operations_data = json.load(data_file)
            except json.JSONDecodeError as ex:
                logger.error(ex)
                return []
            else:
                if type(operations_data) is not list:
                    logger.warning("Processed data is not a list")
                    return []
                logger.info("Data deserialized successfully")
                return operations_data

    except FileNotFoundError as ex:
        logger.error(ex)
        return []


def get_transaction_amount(transaction: dict[str, Any]) -> float:
    """Function that returns transaction amount in rubles."""
    currency = transaction.get("operationAmount").get("currency", {}).get("code")
    amount = float(transaction.get("operationAmount").get("amount"))

    if currency == "RUB":
        logger.info(f"Returning RUB-transaction (id: {transaction.get("id")}) amount")
        return amount
    else:
        logger.info(f"Trying to get amount for {currency}-transaction (id: {transaction.get("id")})")
        status, result = get_exchange_rate(amount, currency)

        if status:
            logger.info(f"Successful exchange operation, transaction amount: {result} RUB")
            return result
