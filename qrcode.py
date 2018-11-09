# для qr кода
from PIL import Image
from pyzbar.pyzbar import decode
qr_code = decode(Image.open(fileName))
cardNum = str(qr_code).split()[0][16:-2]

""""""
# Моя карта
    fileName = str(str(message.chat.id) + '.jpg')
    if message.text == 'Моя карта':
        mycard_keyboard = telebot.types.ReplyKeyboardMarkup()
        mycard_keyboard.row('Узнать баланс', 'Назад')
        bot.send_message(message.from_user.id, "Выберите", reply_markup=mycard_keyboard)
    if message.text == 'Узнать баланс':
        bot.send_message(message.from_user.id, "Отправь фотку QR кода с обратной стороны карты")
        @bot.message_handler(content_types=['photo'])
        def handle_docs_photo(message):
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = '/Users/Ivan/Desktop/GitHub/miemsurfcoffee/telegramBot/' + fileName
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "QRcode обрабатывается")
            qr_code = decode(Image.open(fileName))
            cardNum = str(qr_code).split()[0][16:-2]
            bot.send_message(message.from_user.id, cardNum)
            bot.send_message(message.from_user.id, qr_code)
    if message.text == 'Назад':
        user_keyboard_back = telebot.types.ReplyKeyboardMarkup()
        user_keyboard_back.row('Моя карта', 'Новости')
        user_keyboard_back.row('Кофейни', 'Меню')
        bot.send_message(message.from_user.id, "Выберите", reply_markup=user_keyboard_back)