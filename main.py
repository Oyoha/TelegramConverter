import telebot
from config import keys, TOKEN
from extensions import ConversionExeption, CryptoConvertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helps(message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<Имя валюты, цену которой хотите узнать>'\
           '<Имя валюты, в которой надо узнать цену первой валюты>' \
           '<Количество первой валюты>\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise ConversionExeption('Слишком много параметров')
        elif len(values) < 3:
            raise ConversionExeption('Слишком мало параметров')
        quote, base, amount = values
        total_base = CryptoConvertor.get_price(quote, base, amount)
    except ConversionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base * float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()


