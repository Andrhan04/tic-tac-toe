from telebot import types
from configurate.Logs import write_log
from Class.bot import bot

@bot.message_handler(commands=['start'])
def start_message(message : types.Message):
    bot.send_message(message.chat.id,"Привет ✌️ ")
    get_user(message)

def get_user(message : types.Message):
    print('id пользователя', message.chat.id)
    print('имя пользователя', message.from_user.first_name)
    print('фамилия пользователя', message.from_user.last_name)
    print('никнейм пользователя', message.from_user.username)
    global user
    user.Init_message(message)
    write_log(user,message.text)
    

@bot.message_handler(commands=['button'])
def button_message(message : types.Message):
    markup : types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 : types.KeyboardButton = types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    write_log(user,message.text)

@bot.message_handler(commands=['stop'])
def stop(message : types.Message):
    bot.send_message(message.chat.id, 'Спокойной ночи', reply_markup=types.ReplyKeyboardRemove())
    write_log(user, message.text)
    bot.stop_bot()

@bot.message_handler(content_types='text')
def message_reply(message : types.Message):
    write_log(message)
    if message.text=="Новая игра":
        bot.send_message(message.chat.id,'Будет новая игра',reply_markup=types.ReplyKeyboardRemove())
    elif message.text=="Сделать ход":
        bot.send_message(message.chat.id,'Подожди')
        bot.send_message(message.chat.id,'Едем дальше',reply_markup=types.ReplyKeyboardRemove())
    elif message.text=="ВЫХОД":
        bot.send_message(message.chat.id, 'Спокойной ночи', reply_markup=types.ReplyKeyboardRemove())
        bot.stop_bot()
    else:
        bot.send_message(message.chat.id,f"{message.text}",reply_markup=types.ReplyKeyboardRemove())

print("Бот встал")

bot.infinity_polling()