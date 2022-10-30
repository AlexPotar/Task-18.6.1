import requests
import json

currency_keys = {
    'евро': 'EUR',
    'доллар': 'USD',
    'рубль': 'RUB',
}


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            quote_ticker = currency_keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = currency_keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удается обработать введенное количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        currency_rate = json.loads(r.content)[currency_keys[quote]]

        return currency_rate * amount
