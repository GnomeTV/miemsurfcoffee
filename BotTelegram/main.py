import telebot
import const
bot = telebot.TeleBot(const.token)
# Стандартная клавиатура
@bot.message_handler(commands=['start'])
def handler_start(message):
    user_keyboard = telebot.types.ReplyKeyboardMarkup()
    user_keyboard.row('Моя карта', 'Новости')
    user_keyboard.row('Кафе', 'Меню')
    bot.send_message(message.from_user.id, "Алоха, бро😎", reply_markup=user_keyboard)
# Клавиатура для кнопки (Моя карта)
@bot.message_handler(content_types=['text'])
def press_mycard(message):
    if message.text == 'Моя карта':
        mycard_keyboard = telebot.types.ReplyKeyboardMarkup()
        mycard_keyboard.row('Сделать фото', 'Назад')
        bot.send_message(message.from_user.id, "Выберите", reply_markup=mycard_keyboard)
    if message.text == 'Назад':
        user_keyboard_back = telebot.types.ReplyKeyboardMarkup()
        user_keyboard_back.row('Моя карта', 'Новости')
        user_keyboard_back.row('Кофейни', 'Меню')
        bot.send_message(message.from_user.id, "Выберите", reply_markup=user_keyboard_back)



bot.polling(none_stop=True)
