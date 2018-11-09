import telebot
import const
from telebot import types
import requests
from PIL import Image
from pyzbar.pyzbar import decode
bot = telebot.TeleBot(const.token)

menu = ('''{:-^30}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:-^30}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:-^30}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:-^30}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:-^30}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:-^30}
{:.^} - {}
{:.^} - {}
{:-^30}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:-^30}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:-^30}
{:.^} - {}
{:.^} - {}
{:-^30}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:.^} - {}
{:-^30}
{:.^} - {}
{:-^30}
{:.^} - {}
{:.^} - {}
'''.format('Фирменный Кофе', 'Двойной гавайский', '229/249 ₽', 'Малиновый латте', '229/249 ₽', 'Джинджер', '229/249 ₽', 'Латте теахупу', '229/249 ₽', 'Хайфа кофе', '229/249 ₽', 'Раф-Кофе',
'Классический', '249/279 ₽', 'Пуэрто-риканский', '269/299 ₽',
'Солёная карамель', '249/279 ₽',
'Лавандовый', '269/299 ₽',
'Шоколад',
'Мокко', '219/249 ₽',
'Мятный мокко', '249/279 ₽',
'Какао', '169/189/219 ₽',
'Фирменные Чаи',
'Биарритц', '179/209 ₽',
'Чилин', '179/209 ₽',
'Карелия', '179/209 ₽',
'Пряный чай-латте', '179/209 ₽',
'Иван-чай', '69/99 ₽',
'Go Vegan!',
'Ко вай веган', '229/269/329 ₽',
'Матча латте', '229/269/329 ₽',
'Чёрный латте', '219/249/269 ₽',
'Битберри латте', '229/269/329 ₽',
'Айс манки смузи', '199 ₽',
'Холодный Кофе',
'Айс-латте', '199 ₽',
'Маверик бамбл', '219 ₽',
'Смузи',
'Португальский', '259 ₽',
'Утро на Таити', '259 ₽',
'Бали бум', '259 ₽',
'Лимонады',
'Кейптаун', '199 ₽',
'Кэлли слейтер', '199 ₽',
'Сан-паулу', '199 ₽',
'Милкшейки',
'Ванильный', '259 ₽',
'Орео', '259 ₽',
'Классика Кофе',
'Эспрессо', '99 ₽',
'Американо', '139/169/199 ₽',
'Фильтр-кофе', '139/169/199 ₽',
'Капучино', '149/179/199 ₽',
'Латте', '149/179/199 ₽',
'Флет уайт', '169 ₽',
'Молоко',
'Альтернативное', '50/80/110 ₽',
'Добавки',
'Сироп SURF', '10/20/30 ₽',
'Зефир маршмеллоу / масала ', '50/80 ₽'))

A = ['55.822134,37.384924', '55.771663,37.682658', '55.761076,37.632374', '55.757391,37.622978',
             '55.754033,37.637354', '55.752040,37.670716', '55.745017,37.684479', '55.752604,37.597523',
             '55.742325,37.609997', '55.721476,37.611827', '55.693549,37.557648',
     '55.688152,37.615642', '55.663194,37.481396']
dic = {}
ad = ''
for i in range (len(A)-1):
    ad+=A[i]+'|'
ad+=A[len(A)-1]


def distance_calc(latlon,mode):
    global ad
    a = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + latlon + '&destinations=' + ad + '&mode=' + mode + '&language=ru&key=AIzaSyCcswgpnbZPAP4j1m91NRc2fnBfPO__APM'
    b = {}
    r = requests.get(a, params=b)
    data = r.json()
    err = (data['rows'][0]['elements'][0]['status'])
    if err != 'ZERO_RESULTS':
        distance = data['rows'][0]['elements'][0]['distance']['value']
        ind = 0
        for i in range (1,len(A)):
            if (data['rows'][0]['elements'][i]['distance']['value']) < distance:
                distance = data['rows'][0]['elements'][i]['distance']['value']
                ind = i
        if mode == 'walking':
            time = str(data['rows'][0]['elements'][ind]['duration']['text'])
        else:
            time = str(data['rows'][0]['elements'][ind]['duration_in_traffic']['text'])
        address = data['destination_addresses'][ind]
        return(distance, time, address, ind)
    else:
        return ('','','','')
# Стандартная клавиатура
@bot.message_handler(commands=['start'])
def handler_start(message):
    user_keyboard = telebot.types.ReplyKeyboardMarkup()
    user_keyboard.row('Моя карта', 'Новости')
    user_keyboard.row('Кофейни', 'Меню')
    bot.send_message(message.from_user.id, "Алоха, бро😎", reply_markup=user_keyboard)
# Клавиатура для кнопки (Моя карта)
@bot.message_handler(content_types=['text'])
def press_mycard(message):
    if message.text == 'Меню':
        user_keyboard_back = telebot.types.ReplyKeyboardMarkup()
        user_keyboard_back.row('Моя карта', 'Новости')
        user_keyboard_back.row('Кофейни', 'Меню')
        bot.send_message(message.from_user.id, '%s' %menu, reply_markup=user_keyboard_back)
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
    if message.text == 'Назад':
        user_keyboard_back = telebot.types.ReplyKeyboardMarkup()
        user_keyboard_back.row('Моя карта', 'Новости')
        user_keyboard_back.row('Кофейни', 'Меню')
        bot.send_message(message.from_user.id, "Выберите", reply_markup=user_keyboard_back)
    if message.text == 'Кофейни':
        user_keyboard = telebot.types.ReplyKeyboardMarkup()
        user_keyboard.row('Ближайшая кофейня', 'Посмотреть все адреса')
        bot.send_message(message.from_user.id, "Выберите", reply_markup=user_keyboard)
    if message.text == 'Ближайшая кофейня':
        keyboard = types.ReplyKeyboardMarkup(True)
        button_geo = types.KeyboardButton(text='Отправить геолокацию', request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.from_user.id, 'Отправь мне своё местоположение!', reply_markup=keyboard)
    elif message.text == 'Посмотреть все адреса':
        bot.send_message(message.from_user.id, 'Перейдите по ссылке: https://www.google.com/maps/d/u/0/edit?mid=1uy5NOjQzmv_o0YjL0s17279nTRe35_42&ll=55.773651838993%2C37.51691856768127&z=11')

    else:
        if message.text == 'На машине':
            hide_markup = types.ReplyKeyboardMarkup(True)
            hide_markup.row('Ближайшая кофейня', 'Посмотреть все адреса')
            bot.send_message(message.from_user.id, 'Поиск ближайшей кофейни с учётом пробок...', reply_markup = hide_markup)
            dic[str(message.from_user.id)] = 'driving&departure_time=now'
            if dic.get(message.from_user.id)==None:
                keyboard = types.ReplyKeyboardMarkup(True)
                button_geo = types.KeyboardButton(text='Отправить местоположение', request_location=True)
                keyboard.add(button_geo)
                bot.send_message(message.from_user.id, 'Произошла ошибка')
                bot.send_message(message.from_user.id, 'Пожалуйста отправьте свои координаты', reply_markup=keyboard)

        elif message.text == 'Пешком':
            hide_markup = types.ReplyKeyboardMarkup(True)
            hide_markup.row('Ближайшая кофейня', 'Посмотреть все адреса')
            dic[str(message.from_user.id)] = 'walking'
            bot.send_message(message.from_user.id, 'Поиск ближайшей кофейни...', reply_markup = hide_markup)
            if dic.get(message.from_user.id)==None:
                keyboard = types.ReplyKeyboardMarkup(True)
                button_geo = types.KeyboardButton(text='Отправить местоположение', request_location=True)
                keyboard.add(button_geo)
                bot.send_message(message.from_user.id, 'Произошла ошибка')
                bot.send_message(message.from_user.id, 'Пожалуйста отправьте свои координаты', reply_markup=keyboard)

        if dic.get(message.from_user.id)!=None:
            distance, time, address, ind = distance_calc(dic[message.from_user.id], dic[str(message.from_user.id)])
            if distance != '':

                st = A[ind].split(',')
                bot.send_location(message.from_user.id, float(st[0]),float(st[1]))
                bot.send_message(message.from_user.id,'Адрес ближайшего SurfCoffee: %s.' %address)
                bot.send_message(message.from_user.id, 'Ваше расстояние до ближайшего SurfCoffee: %s м.' %distance)
                bot.send_message(message.from_user.id, 'Время в пути до ближайшего SurfCoffee: %s' %time )
                del dic[message.from_user.id]
                del dic[str(message.from_user.id)]
            else:
                bot.send_message(message.from_user.id, 'Невозможно проложить маршрут!')
                del dic[message.from_user.id]
                del dic[str(message.from_user.id)]

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        hide_markup = types.ReplyKeyboardMarkup(True)
        hide_markup.row('На машине', 'Пешком')
        bot.send_message(message.from_user.id, 'Спасибо!', reply_markup=hide_markup)
        bot.send_message(message.from_user.id, 'Как ты будешь добираться до SurfCoffee?')
        dic[message.from_user.id] = str(message.location.latitude) + ',' + str(message.location.longitude)

bot.polling(none_stop=True)