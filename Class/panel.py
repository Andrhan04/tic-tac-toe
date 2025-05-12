from Class.bot import bot
from telebot import types


data = ["Авторизация", "Новая игра"]

def get(message : types.Message):
    markup : types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in data:
        items : types.KeyboardButton = types.KeyboardButton(i)
        markup.add(items)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

data_game = ["Посмотреть поле", "Сделать ход", "Завершить игру", "Новая игра"]

def Game(message : types.Message):
    markup : types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in data_game:
        items : types.KeyboardButton = types.KeyboardButton(i)
        markup.add(items)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)


data_admin = ["/stop", "Сделай лучший ход от Доржи", "Сделай лучший ход от IT Planet", "Лучший ход по мнению Доржи", "Лучший ход по мнению IT Planet"]

def Admin(message : types.Message):
    markup : types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in data_admin:
        items : types.KeyboardButton = types.KeyboardButton(i)
        markup.add(items)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)