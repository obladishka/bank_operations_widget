import importlib
import os

from src.generators import filter_by_currency
from src.processing import filter_by_state, search_by_srt, sort_by_date
from src.widget import get_date, mask_account_card


def main():
    """Main function for app usage."""

    base_path = os.path.join(os.path.dirname(__file__), "data")

    commands = {
        "1": {"format": "JSON", "file_name": "operations.json"},
        "2": {"format": "CSV", "file_name": "transactions.csv"},
        "3": {"format": "Excel", "file_name": "transactions_excel.xlsx"},
    }

    print(
        """Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла\n"""
    )

    user_input = input("Ввод: ")

    user_choice = commands.get(user_input)

    if not user_choice:
        print("Я не знаю такой команды")
        return

    # calling relevant func according to user input
    file_format = user_choice["format"]
    file_path = os.path.join(base_path, user_choice["file_name"])
    module_name = "src.utils" if user_choice["format"] == "JSON" else "src.read_from_file"
    module = importlib.import_module(module_name)
    func_name = getattr(module, f"get_operations_data_from_{file_format.lower()}")
    print(f"Для обработки выбран {file_format}-файл.\n")

    transactions = func_name(file_path)

    statuses_list = ["EXECUTED", "CANCELED", "PENDING"]
    print(
        """Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"""
    )

    raw_user_input = input("Ввод: ")
    user_input = raw_user_input.upper()

    while user_input not in statuses_list:
        print(f'Статус операции "{raw_user_input}" недоступен.')
        print(
            """Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"""
        )
        raw_user_input = input("Ввод: ")
        user_input = raw_user_input.upper()

    print(f"\nОперации отфильтрованы по статусу {raw_user_input}")
    filtered_transactions = filter_by_state(transactions, user_input)

    is_sort_by_date = input("\nОтсортировать операции по дате? Да/Нет ")
    if is_sort_by_date.lower() == "да":
        parameter = (
            False if input("\nОтсортировать по возрастанию или по убыванию? ").lower() == "по возрастанию" else True
        )
        filtered_transactions = sort_by_date(filtered_transactions, parameter)

    is_sort_by_currency = input("\nВыводить только рублевые транзакции? Да/Нет ")
    if is_sort_by_currency.lower() == "да":
        filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))

    is_filter_by_word = input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет ")
    if is_filter_by_word.lower() == "да":
        search_word = input("\nВведите слово для поиска: ").split()[0]
        filtered_transactions = search_by_srt(filtered_transactions, search_word)

    print("\nРаспечатываю итоговый список транзакций...")

    if len(filtered_transactions) == 0 or filtered_transactions == "State is invalid":
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)}\n")

        for transaction in filtered_transactions:
            date = get_date(transaction.get("date"))
            description = transaction.get("description")
            to_card = mask_account_card(transaction.get("to"))
            amount = " ".join(
                [
                    str(transaction.get("operationAmount", {}).get("amount")),
                    transaction.get("operationAmount", {}).get("currency", {}).get("name"),
                ]
            )

            if transaction.get("from") is not None:
                from_card = mask_account_card(transaction.get("from"))
                print(f"{date} {description}\n{from_card} -> {to_card}\nСумма: {amount}\n")
            else:
                print(f"{date} {description}\n{to_card}\nСумма: {amount}\n")


if __name__ == "__main__":
    main()
