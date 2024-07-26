import json
from typing import Any

from src.external_api import get_exchange_rate


def get_operations_data(file_path: str) -> list[dict]:
    """Function that returns info about financial transactions from JSON-file."""
    try:
        with open(file_path, "r", encoding="utf-8") as data_file:

            try:
                operations_data = json.load(data_file)
            except json.JSONDecodeError:
                return []
            else:
                return operations_data

    except FileNotFoundError:
        return []


def get_transaction_amount(transaction: dict[str, Any]) -> float:
    """Function that returns transaction amount in rubles."""
    currency = transaction.get("operationAmount").get("currency", {}).get("code")
    amount = float(transaction.get("operationAmount").get("amount"))

    if currency == "RUB":
        return amount
    else:
        status, result = get_exchange_rate(amount, currency)
        if status:
            return result
