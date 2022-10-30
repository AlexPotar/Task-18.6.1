import telebot
from config import TOKEN
from extensions import currency_keys, APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду для бота в следующем формате:\
    <имя валюты цену которой вы хотите узнать>\
    <имя валюты в которой надо узнать цену первой валюты> \
    <количество переводимой валюты>\n\nПросмотреть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency_keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        params = message.text.split(' ')

        if len(params) != 3:
            raise APIException('Неверное количество параметров (должно быть 3)')

        base, quote, amount = params
        amount_quote = CurrencyConverter.get_price(base, quote, amount)

        text = f'Цена {amount} {base} в {quote} равна {amount_quote}'
        bot.send_message(message.chat.id, text)
    except Exception as ex:
        bot.send_message(message.chat.id, f"Ошибка, тип: {type(ex).__name__}\n{str(ex)}")


bot.polling()
