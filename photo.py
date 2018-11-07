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
        mycard_keyboard.row('Назад')
        bot.send_message(message.from_user.id, "Отправьте фото QRcode", reply_markup=mycard_keyboard)

        #здеь начинвется мой код
        @bot.message_handler(content_types=['photo'])
        def handle_docs_photo(message):
            try:
                file_info = bot.get_file(message.photo[0].file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                src = '/Desktop/Berry Sky/untitled1/abc/' + message.photo[0].file_id
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.reply_to(message, "Фото добавлено")

            except Exception as e:
                bot.reply_to(message, e)
        #здесь заканчивается мой код

    if message.text == 'Назад':
        user_keyboard_back = telebot.types.ReplyKeyboardMarkup()
        user_keyboard_back.row('Моя карта', 'Новости')
        user_keyboard_back.row('Кофейни', 'Меню')
        bot.send_message(message.from_user.id, "Выберите", reply_markup=user_keyboard_back)



bot.polling(none_stop=True)