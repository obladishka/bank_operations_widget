def filter_by_currency(transactions_list, currency):
    """Function that filters transactions in a specified currency."""
    filtered_transactions = list(
        filter(
            lambda transaction: transaction.get("operationAmount").get("currency", {}).get("code") == currency,
            transactions_list,
        )
    )

    if not transactions_list or len(filtered_transactions) == 0:
        return "No transactions in such currency"

    return iter(filtered_transactions)


def transaction_descriptions(transactions_list):
    """Function that returns description of each transaction in turn."""
    if not transactions_list:
        yield "No transactions found"

    descriptions = (
        transaction.get("description", "Operation description is not defined") for transaction in transactions_list
    )
    for description in descriptions:
        yield description


def card_number_generator(start, stop):
    """Function that generates cards numbers within specified range."""
    min_number, max_number = 1, 9999999999999999
    if start > stop:
        yield "Min range should be smaller than max range"
    elif start < min_number or stop > max_number:
        yield "Range should be between 1 and 9999999999999999"

    for i in range(start, stop + 1):
        number_str = "{:016}".format(min_number + i - 1)
        yield " ".join([number_str[x : x + 4] for x in range(0, len(number_str), 4)])
