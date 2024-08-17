import re
from collections import Counter
from datetime import datetime


def filter_by_state(
    operations_data: list[dict[str, str | int]], state: str = "EXECUTED"
) -> list[dict[str, str | int]] | str:
    """Function that filters information by a specified criteria."""
    if not operations_data:
        return []
    elif state not in [operation.get("state") for operation in operations_data]:
        return "State is invalid"
    return [operation for operation in operations_data if operation.get("state") == state]


def sort_by_date(operations_data: list[dict[str, str | int]], parameter: bool = True) -> list[dict[str, str | int]]:
    """Function that sorts information by date."""
    for index, info in enumerate(operations_data):
        if info.get("date") is None:
            operations_data.pop(index)
            print(f"Operation {info.get("id")} date is unknown")
        else:
            try:
                datetime.fromisoformat(str(info.get("date")))
            except ValueError:
                operations_data.pop(index)
                print(f"Operation {info.get("id")} date should be in format YYYY-MM-DD")
    return sorted(operations_data, key=lambda date: date["date"], reverse=parameter)


def search_by_srt(operations_data: list[dict], search_str: str) -> list[dict]:
    """Function that filters transaction by a specified word in description."""
    pattern = rf"{re.escape(re.sub(r"ть|сти|вать", "", search_str))}?.*"
    return [
        operation
        for operation in operations_data
        if re.search(pattern, operation.get("description", ""), flags=re.IGNORECASE)
    ]


def analyze_categories(operations_data: list[dict], categories_list: list[str]) -> dict:
    """Function that counts number of transactions of each category."""
    descriptions_list = [operation.get("description") for operation in operations_data]
    descriptions_count = Counter(descriptions_list)
    result = {}

    for category in categories_list:
        result[category] = descriptions_count.get(category, 0)

    return result
