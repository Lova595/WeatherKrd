from telebot import types
import parser_weather


def create_main_bottom():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    touch_weather = types.KeyboardButton('Узнать погоду')
    touch_play = types.KeyboardButton('Играть')
    markup.add(touch_weather, touch_play)
    return markup


def create_weather_bottom():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    touch_today = types.KeyboardButton('Сегодня')
    touch_tomorrow = types.KeyboardButton('Завтра')
    touch_week = types.KeyboardButton('На неделю')
    touch_day_off = types.KeyboardButton('На выходные')
    touch_on_main = types.KeyboardButton('Главное меню')
    markup.add(touch_today, touch_tomorrow, touch_week, touch_day_off, touch_on_main)
    return markup


def create_interval_bottom():
    inline_markup = types.InlineKeyboardMarkup(row_width=True)  # row_width с True по одной на каждой строке
    touch_night = types.InlineKeyboardButton('Ночь 🌃', callback_data='night')
    touch_morning = types.InlineKeyboardButton('Утро 🌅', callback_data='morning')
    touch_day = types.InlineKeyboardButton('День 🏙', callback_data='day')
    touch_evening = types.InlineKeyboardButton('Вечер 🌆', callback_data='evening')
    inline_markup.add(touch_night, touch_morning, touch_day, touch_evening)
    return inline_markup


def create_back_bottom(x):
    inline_markup = types.InlineKeyboardMarkup(row_width=True)
    touch_back = types.InlineKeyboardButton('Назад', callback_data=f'back {x}')
    inline_markup.add(touch_back)
    return inline_markup


def create_details_bottom_today():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    touch_recommendation = types.KeyboardButton('Рекомендация')
    touch_calendar = types.KeyboardButton('Народный календарь 🌤')
    touch_back_menu = types.KeyboardButton('Главное меню')
    touch_back = types.KeyboardButton('Назад')
    markup.add(touch_calendar)
    markup.add(touch_recommendation, touch_back_menu, touch_back)
    return markup


def create_details_bottom_tomorrow():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    touch_recommendation = types.KeyboardButton('Рекомендация')
    touch_calendar = types.KeyboardButton('Народный календарь ⛅')
    touch_back_menu = types.KeyboardButton('Главное меню')
    touch_back = types.KeyboardButton('Назад')
    markup.add(touch_calendar)
    markup.add(touch_recommendation, touch_back_menu, touch_back)
    return markup


def create_play_bottom():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    touch_back = types.KeyboardButton('Главное меню')
    markup.add(touch_back)
    return markup


def show_weather_time(x: int, z: int, t: str):
    content, temp, description, folk = parser_weather.start('today')
    text = f'{t}\nТемпература, °C: '
    flag = True
    for i in temp:
        i = i.split('°')
        for y in i[x:z]:
            text += f' {y}'
        if flag:
            text += '\nЧувствуется как: '
            flag = False
    return text
