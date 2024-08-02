import pandas as pd


def get_operations_data_from_csv(file_path: str) -> list[dict]:
    """Function that returns info about financial transactions from CSV-file in JSON-format."""
    try:
        df = pd.read_csv(file_path, delimiter=";")
        operations_dict = df.fillna(0).to_dict(orient="records")
        formated_dict = [
            {
                "id": i.get("id"),
                "state": i.get("state"),
                "date": i.get("date"),
                "operationAmount": {
                    "amount": i.get("amount"),
                    "currency": {"name": i.get("currency_name"), "code": i.get("currency_code")},
                },
                "description": i.get("description"),
                "from": i.get("from"),
                "to": i.get("to"),
            }
            for i in operations_dict
        ]

        for operation in formated_dict:
            for key, value in list(operation.items()):
                if value == 0:
                    del operation[key]

        return formated_dict

    except FileNotFoundError:
        return []
