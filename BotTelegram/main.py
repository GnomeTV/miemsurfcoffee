import telebot
import const
from telebot import types
import requests
bot = telebot.TeleBot(const.token)
A = ['55.822134,37.384924', '55.771663,37.682658', '55.761076,37.632374', '55.757391,37.622978',
             '55.754033,37.637354', '55.752040,37.670716', '55.745017,37.684479', '55.752604,37.597523',
             '55.742325,37.609997', '55.721476,37.611827', '55.693549,37.557648',
     '55.688152,37.615642', '55.663194,37.481396']
lat = ''
lon = ''
ad = ''
for i in range (len(A)-1):
    ad+=A[i]+'|'
ad+=A[len(A)-1]


def distance_calc(lat1,lon1,mode):
    global ad
    a = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + lat1 + ',' + lon1 + '&destinations=' + ad + '&mode=' + mode + '&language=ru&key=AIzaSyCcswgpnbZPAP4j1m91NRc2fnBfPO__APM'
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
    if message.text == 'Моя карта':
        mycard_keyboard = telebot.types.ReplyKeyboardMarkup()
        mycard_keyboard.row('Сделать фото', 'Назад')
        bot.send_message(message.from_user.id, "Выберите", reply_markup=mycard_keyboard)
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
            s = 'driving&departure_time=now'
            if lat=='':
                keyboard = types.ReplyKeyboardMarkup(True)
                button_geo = types.KeyboardButton(text='Отправить местоположение', request_location=True)
                keyboard.add(button_geo)
                bot.send_message(message.from_user.id, 'Произошла ошибка')
                bot.send_message(message.from_user.id, 'Пожалуйста отправьте свои координаты', reply_markup=keyboard)

        elif message.text == 'Пешком':
            hide_markup = types.ReplyKeyboardMarkup(True)
            hide_markup.row('Ближайшая кофейня', 'Посмотреть все адреса')
            s = 'walking'
            bot.send_message(message.from_user.id, 'Поиск ближайшей кофейни...', reply_markup = hide_markup)
            if lat=='':
                keyboard = types.ReplyKeyboardMarkup(True)
                button_geo = types.KeyboardButton(text='Отправить местоположение', request_location=True)
                keyboard.add(button_geo)
                bot.send_message(message.from_user.id, 'Произошла ошибка')
                bot.send_message(message.from_user.id, 'Пожалуйста отправьте свои координаты', reply_markup=keyboard)

        if lat!='':
            distance, time, address, ind = distance_calc(lat, lon , s)
            if distance != '':

                st = A[ind].split(',')
                bot.send_location(message.from_user.id, float(st[0]),float(st[1]))
                bot.send_message(message.from_user.id,'Адрес ближайшего SurfCoffee: %s.' %address)
                bot.send_message(message.from_user.id, 'Ваше расстояние до ближайшего SurfCoffee: %s м.' %distance)
                bot.send_message(message.from_user.id, 'Время в пути до ближайшего SurfCoffee: %s' %time )
            else:
                bot.send_message(message.from_user.id, 'Невозможно проложить маршрут!')

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        hide_markup = types.ReplyKeyboardMarkup(True)
        hide_markup.row('На машине', 'Пешком')
        bot.send_message(message.from_user.id, 'Спасибо!', reply_markup=hide_markup)
        bot.send_message(message.from_user.id, 'Как ты будешь добираться до SurfCoffee?')
        global lat, lon
        lat = str(message.location.latitude)
        lon = str(message.location.longitude)



bot.polling(none_stop=True)
