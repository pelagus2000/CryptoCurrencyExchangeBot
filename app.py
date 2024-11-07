import telebot
from config import keys, TOKEN
from utils import CryptoConverter, ConvertionExceptions

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	text = ("Чтобы начать работу введите команту боту в следующем формате: \n <имя валюты> \n "
			"<в какую валюту перевести> \n <количество валюты> \n <Увидеть список всех доступных валют: /values >")
	bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message):
	text1 = 'доступные валюты:'
	for key in keys.keys():
		text1 = '\n'. join((text1, key, ))
	bot.reply_to(message, text1)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
	try:
		values = message.text.split(' ')

		if len(values) != 3:
			raise ConvertionExceptions("Слишком много параметров")

		quote, base, amount = values

		total_base = CryptoConverter.convert(quote, base, amount)
	except ConvertionExceptions as e:
		bot.reply_to(message, f'Ошибка пользователя\n{e}')
	except Exception as e:
		bot.reply_to(message, f'Не удалось отработать команду\n{e}')
	else:
		text = f'Цена {amount} {quote} в {base} - {total_base}'
		bot.send_message(message.chat.id, text)


bot.infinity_polling()