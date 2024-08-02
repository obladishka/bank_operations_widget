from unittest.mock import patch

from src.read_from_file import get_operations_data_from_csv


@patch("src.read_from_file.pd.read_csv")
@patch("src.read_from_file.open")
def test_get_operations_data_from_csv(mock_open, mock_read_csv, get_df):
    """Tests normal work of get_operations_data_from_csv function."""
    mock_read_csv.return_value = get_df
    assert get_operations_data_from_csv("existing.csv")[:2] == [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "operationAmount": {"amount": 16210, "currency": {"name": "Sol", "code": "PEN"}},
            "description": "Перевод организации",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
        },
        {
            "id": 5380041,
            "state": "CANCELED",
            "date": "2021-02-01T11:54:58Z",
            "operationAmount": {"amount": 23789, "currency": {"name": "Peso", "code": "UYU"}},
            "description": "Открытие вклада",
            "to": "Счет 23294994494356835683",
        },
    ]
    mock_read_csv.assert_called_once_with("existing.csv", delimiter=";")


def test_get_operations_data_from_csv_no_such_file():
    """Tests get_operations_data_from_csv function when a CSV-file does not exist."""
    file_name = "no_such_file.csv"
    assert get_operations_data_from_csv(file_name) == []
