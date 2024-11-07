import requests
import json
from config import keys

class ConvertionExceptions(Exception):
	pass

class CryptoConverter:
	@staticmethod
	def convert(quote: str, base: str, amount: str):
		if quote == base:
			raise ConvertionExceptions(f'Невозможно перевести одинаковые валюты {base}')

		try:
			quote_ticker = keys[quote]
		except KeyError:
			raise ConvertionExceptions(f'Не удалось отработать валюту {quote}')

		try:
			base_ticker = keys[base]
		except KeyError:
			raise ConvertionExceptions(f'Не удалось отработать валюту {base}')

		try:
			amount == float(amount)
		except ValueError:
			raise ConvertionExceptions(f'Не удалось отработать количество {amount}')

		quote_ticker, base_ticker = keys[quote], keys[base]

		r = requests.get(
			f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
		total_base = json.loads(r.content)[keys[base]]


		return total_base