import telebot

TOKEN = '6226253771:AAEaRAnOx63kbSVkST3c4HzB804Y4XR47co'

# аргумент parce_mode, скорее всего, будет другой
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['hello-world'])
def test_message(message):
    bot.send_message(message.chat.id, 'Если вы видите это сообщение, значит все работает.')


@bot.message_handler(func=lambda message: message.text.lower() == 'привет')
def test_hello_message(message):
    bot.reply_to(message, 'Привет!')


if __name__ == '__main__':
    bot.infinity_polling()