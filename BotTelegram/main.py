import telebot
import const


bot = telebot.TeleBot(const.token)
# Basic KeyBoard
@bot.message_handler(commands=['start'])
def handler_start(message):
    user_keyboard = telebot.types.ReplyKeyboardMarkup()
    user_keyboard.row('My card', 'News')
    user_keyboard.row('Cafes', 'Menu')
    bot.send_message(message.from_user.id, "Aloha, doggy", reply_markup=user_keyboard)
# KeyBoard for button My Card
@bot.message_handler(content_types=['text'])
def press_mycard(message):
    if message.text == 'My card':
        mycard_keyboard = telebot.types.ReplyKeyboardMarkup()
        mycard_keyboard.row('Enter number card', 'Back')
        bot.send_message(message.from_user.id, "What do you want?", reply_markup=mycard_keyboard)

@bot.message_handler(content_types=['text'])
def message_back(message):
    if message.text == 'Back':
        user_keyboard_back = telebot.types.ReplyKeyboardMarkup()
        user_keyboard_back.row('My card', 'News')
        user_keyboard_back.row('Cafes', 'Menu')
        bot.send_message(message.from_user.id, "Aloha, doggy", reply_markup=user_keyboard_back)
bot.polling(none_stop=True)
