def filter_by_state(
    operations_data: list[dict[str, str | int]], state: str = "EXECUTED"
) -> list[dict[str, str | int]]:
    """Function that filters information by a specified criteria."""
    return [operation for operation in operations_data if operation.get("state") == state]


def sort_by_date(operations_data: list[dict[str, str | int]], parameter: bool = True) -> list[dict[str, str | int]]:
    """Function that sorts information by date."""
    return sorted(operations_data, key=lambda date: date["date"], reverse=parameter)
