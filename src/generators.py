def filter_by_currency(transactions_list, currency):
    """Function that filters transactions in a specified currency."""
    try:
        filtered_transactions = list(
            filter(
                lambda transaction: transaction.get("operationAmount").get("currency").get("code") == currency,
                transactions_list,
            )
        )
    except AttributeError:
        return "Transactions currency is not defined"
    else:
        if not transactions_list or len(filtered_transactions) == 0:
            return "No transactions in such currency"
        return filter(
            lambda transaction: transaction.get("operationAmount").get("currency").get("code") == currency,
            transactions_list,
        )
