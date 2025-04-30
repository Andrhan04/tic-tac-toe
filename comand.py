from main import bot
from telebot import types

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет ✌️ ")

@bot.message_handler(commands=['button'])
def button_message(message):
    markup : types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 : types.KeyboardButton = types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id, 'Спокойной ночи', reply_markup=types.ReplyKeyboardRemove())
    bot.stop_bot()