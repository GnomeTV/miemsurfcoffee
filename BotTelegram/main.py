import telebot
import const

bot = telebot.TeleBot(const.token)
@bot.message_handler(commands=['start'])
def handler_start(message):
    user_keyboard = telebot.types.ReplyKeyboardMarkup()
    user_keyboard.row('My card', 'News')
    user_keyboard.row('Cafes', 'Menu')
    bot.send_message(message.from_user.id, "Aloha, doggy", reply_markup=user_keyboard)


bot.polling(none_stop=True)
