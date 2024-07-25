import json


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
