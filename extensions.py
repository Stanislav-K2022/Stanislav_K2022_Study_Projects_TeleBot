import json
import requests
from config import exchanges

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        r = requests.get(f"https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH,DASH&tsyms=BTC,USD,EUR&api_key=0042c7241a0c7a82c070eff68b25ed32355f5060efcc868a3c6ff851bb51d2bb
")
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * amount
        new_price = round(new_price, 3)
        message =  f"Цена {amount} {base} в {sym} : {new_price}"
        return message
