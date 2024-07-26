import os

import requests
from dotenv import load_dotenv


def get_exchange_rate(amount: float, from_currency: str, to_currency: str = "RUB") -> tuple[bool, float | str]:
    """Function that accesses external API to get the current exchange rate."""
    load_dotenv()

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"

    headers = {"apikey": os.getenv("API_KEY")}

    try:
        response = requests.get(url, headers=headers)
        status_code = response.status_code

        if status_code == 200:
            return True, round(response.json()["result"], 2)

        return False, str(response.reason)

    except requests.exceptions.RequestException as ex:
        return False, str(ex)
