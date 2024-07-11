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
