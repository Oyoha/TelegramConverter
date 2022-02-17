import requests
import json
from config import keys


class ConversionExeption(Exception):
    pass


class CryptoConvertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionExeption(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise ConversionExeption(f'Не удалось обработать валюту {quote}')

        try:
            base_ticket = keys[base]
        except KeyError:
            raise ConversionExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionExeption(f'Не удалось обработать количество {amount}')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticket}&tsyms={base_ticket}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base