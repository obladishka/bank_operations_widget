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
