from Class.bot import bot
from telebot import types


data = ["Авторизация", "Новая игра"]

def get(message : types.Message):
    markup : types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in data:
        items : types.KeyboardButton = types.KeyboardButton(i)
        markup.add(items)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

data_game = ["Посмотреть поле", "Сделать ход", "Завершить игру"]

def Game(message : types.Message):
    markup : types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in data_game:
        items : types.KeyboardButton = types.KeyboardButton(i)
        markup.add(items)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)