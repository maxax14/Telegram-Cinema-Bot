import telebot
import time
import logging
from telebot import apihelper
from telebot import types

from src import keys
from src import config
from src.parser import Parser

parser = Parser()
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

apihelper.proxy = {
    'https': keys.TG_PROXY_KEY
}

bot = telebot.AsyncTeleBot(keys.TG_API_TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, config.START_MSG)


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id, config.HELP_MSG)


@bot.message_handler(regexp=r"\/i\d+")
def handle_imdb_id(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Узнать больше", callback_data="show_more")
    watch_button = types.InlineKeyboardButton(text="Смотреть онлайн", callback_data="watch")
    keyboard.add(callback_button)
    keyboard.add(watch_button)

    parser.parse_id(int(message.json['text'][2:]))
    response, photo = parser.output, parser.photo

    if photo is not None:
        bot.send_message(message.chat.id,
                         "[​​​​​​​​​​​]({}) {}".format(photo, response),
                         parse_mode='markdown', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, response, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == "show_more":
            callback_button = types.InlineKeyboardButton(text="Коротко", callback_data="show_less")
            watch_button = types.InlineKeyboardButton(text="Смотреть онлайн", callback_data="watch")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(callback_button)
            keyboard.add(watch_button)
            response, photo = parser.full_output, parser.photo
            if photo is not None:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="[​​​​​​​​​​​]({}) {}".format(photo, response), parse_mode='markdown',
                                      reply_markup=keyboard)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=response, reply_markup=keyboard)
        if call.data == "show_less":
            callback_button = types.InlineKeyboardButton(text="Узнать больше", callback_data="show_more")
            watch_button = types.InlineKeyboardButton(text="Смотреть онлайн", callback_data="watch")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(callback_button)
            keyboard.add(watch_button)
            response, photo = parser.output, parser.photo
            if photo is not None:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="[​​​​​​​​​​​]({}) {}".format(photo, response), parse_mode='markdown',
                                      reply_markup=keyboard)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=response, reply_markup=keyboard)
        if call.data == "watch":
            back_button = types.InlineKeyboardButton(text="Назад", callback_data="show_less")
            ivi_button = types.InlineKeyboardButton(text="💰 IVI", url=config.LINK_IVI + parser.name)
            okko_button = types.InlineKeyboardButton(text="💰 OKKO", url=config.LINK_OKKO + parser.name)
            kp_button = types.InlineKeyboardButton(text="💰 KINOPOISK", url=config.link_kinopoisk(parser.id))
            fs_button = types.InlineKeyboardButton(text="🆓 FS", url=config.LINK_FS + parser.name)
            hd_button = types.InlineKeyboardButton(text="🆓 HDREZKA", url=config.LINK_HDREZKA + parser.name)
            ba_button = types.InlineKeyboardButton(text="🆓 BASKINO", url=config.LINK_BASKINO + parser.name)

            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(back_button)
            keyboard.add(ivi_button, okko_button, kp_button)
            keyboard.add(fs_button, hd_button, ba_button)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=config.WATCH_MSG, reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    response = parser.parse_text(message.json['text'])
    bot.send_message(message.chat.id, response)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, )
        except Exception as e:
            logger.error(e)
            time.sleep(15)
