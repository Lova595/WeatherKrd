import telebot
from random import choice, shuffle
from config import TOKEN
from other import *
import parser_weather
from datetime import datetime

bot = telebot.TeleBot(TOKEN)

all_cities = {'Якутск': 'https://sinoptik.ua/погода-якутск',
              'Магадан': 'https://sinoptik.ua/погода-магадан',

              'Афины': 'https://sinoptik.ua/погода-афины',
              'Нью-Йорк': 'https://sinoptik.ua/погода-нью-йорк',
              'Москва': 'https://sinoptik.ua/погода-москва',
              'Рим': 'https://sinoptik.ua/погода-рим',
              'Каир': 'https://sinoptik.ua/погода-каир',
              'Пекин': 'https://sinoptik.ua/погода-пекин',
              'Токио': 'https://sinoptik.ua/погода-токио',
              'Великий-Устюг': 'https://sinoptik.ua/погода-великий-устюг'
              }
database = {}


@bot.message_handler(commands=['start'])
def welcome_bot(message):
    with open('items/погода.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, f'Привет, {message.chat.first_name}!')
    bot.send_message(message.chat.id, 'Я расскажу тебе, какая погода за окном и дам рекомендации, какую одежду лучше '
                                      'надеть сегодня или завтра по погоде. Еще мы можем сыграть с тобой в игру '
                                      'по предсказанию температуры на следующий день! '
                                      'Выбери что тебя интересует:', reply_markup=create_main_bottom())


@bot.message_handler(content_types=['text'])
def manager_commands(message):
    if message.text == 'Узнать погоду':
        bot.send_message(message.chat.id, 'Выберите нужный период или дату:', reply_markup=create_weather_bottom())

    elif message.text.split()[0] == 'Сегодня':
        content, temp, description, folk = parser_weather.start('today')
        text = ''
        photo_path = ''
        for i in content[0].items():
            text += f'{i[1]}\n'
            if i[0] == 'description':
                i = i[1].lower().replace("\n", " ").strip()
                time = datetime.now().strftime('%H')
                if int(time) < 18:
                    photo_path = f'items/day/{i}.png'
                else:
                    photo_path = f'items/night/{i}.png'
        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=create_details_bottom_today())
        bot.send_message(message.chat.id, text, reply_markup=create_interval_bottom())

    elif message.text == 'Завтра':
        content, temp, description, folk = parser_weather.start('tomorrow')
        text = ''
        photo_path = ''
        for i in content[1].items():
            text += f'{i[1]}\n'
            if i[0] == 'description':
                i = i[1].lower().replace("\n", " ").strip()
                time = datetime.now().strftime('%H')
                if int(time) < 18:
                    photo_path = f'items/day/{i}.png'
                else:
                    photo_path = f'items/night/{i}.png'
        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=create_details_bottom_tomorrow())
        bot.send_message(message.chat.id, text, reply_markup=create_interval_bottom())

    elif message.text == 'На неделю':
        content, temp, description, folk = parser_weather.start('today')
        for i in content:
            text = ''
            for y in i.items():
                text += f'{y[1]}\n'
            bot.send_message(message.chat.id, text)

    elif message.text == 'На выходные':
        content, temp, description, folk = parser_weather.start('today')
        count = 0
        for i in content:
            for k, v in i.items():
                text = ''
                if (v.lower().endswith('воскресенье') or v.lower().endswith('суббота')) and count < 2:
                    for y in i.values():
                        text += f'{y}\n'
                    count += 1
                    bot.send_message(message.chat.id, text)

    elif message.text == 'Народный календарь 🌤':
        content, temp, description, folk = parser_weather.start('today')
        bot.send_message(message.chat.id, folk)

    elif message.text == 'Народный календарь ⛅':
        content, temp, description, folk = parser_weather.start('tomorrow')
        bot.send_message(message.chat.id, folk)

    elif message.text == 'Играть':
        bot_choice = choice(list(all_cities))
        database[message.chat.id] = bot_choice
        answer = bot.send_message(message.chat.id, f'Угадай какая погода сейчас в городе *{bot_choice}*? '
                                                   f'Укажи температуру в градусах Цельсия:',
                                  reply_markup=create_play_bottom(), parse_mode='MARKDOWN')
        bot.register_next_step_handler(answer, check_user_answer)

    elif message.text == 'Главное меню':
        bot.send_message(message.chat.id,
                         'Я расскажу тебе, какая погода за окном и дам рекомендации, какую одежду лучше '
                         'надеть сегодня или завтра по погоде. Еще мы можем сыграть с тобой в игру '
                         'по предсказанию температуры на следующий день! '
                         'Выбери что тебя интересует:', reply_markup=create_main_bottom())

    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Выберите нужный период или дату:', reply_markup=create_weather_bottom())


@bot.callback_query_handler(func=lambda call: True)
def manager_inline_commands(call):
    if call.data == 'night':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=show_weather_time(0, 2, 'Ночь с 0:00 до 3:00'),
                              reply_markup=create_back_bottom(call.data))

    elif call.data == 'morning':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=show_weather_time(2, 4, 'Утро с 6:00 до 9:00'),
                              reply_markup=create_back_bottom(call.data))

    elif call.data == 'day':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=show_weather_time(4, 6, 'День с 12:00 до 15:00'),
                              reply_markup=create_back_bottom(call.data))

    elif call.data == 'evening':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=show_weather_time(6, 8, 'Вечер с 18:00 до 21:00'),
                              reply_markup=create_back_bottom(call.data))

    elif call.data.split()[0] == 'back':
        content, temp, description, folk = parser_weather.start('today')
        text = ''
        for i in content[0].items():
            text += f'{i[1]}\n'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text,
                              reply_markup=create_interval_bottom())


def check_user_answer(message):
    try:
        user_choice = int(message.text)
        real_temp = parser_weather.game_guess_temp(all_cities[database[message.chat.id]])
        if real_temp == user_choice:
            bot.send_message(message.chat.id, f'Поздравляем! Вы угадали! В качестве приза ловите фразу дня:\n'
                                              f'*{parser_weather.get_phrase_day()}*', parse_mode='MARKDOWN')
        else:
            bot.send_message(message.chat.id, 'Вы не угадали!')
        del database[message.chat.id]
    except:
        print('ошибка')
        del database[message.chat.id]



if __name__ == '__main__':
    print('Бот в сети')
    bot.polling(non_stop=True)
