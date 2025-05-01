from telebot import types
from configurate.Logs import write_log
from Class.bot import bot
from Class.Query import IsHost
from Class import User as user
import Class.panel as Panel
from Class.Query import conn

@bot.message_handler(commands=['start'])
def start_message(message : types.Message):
    bot.send_message(message.chat.id,"Привет ✌️ ")
    bot.send_message(message.chat.id,"Нажми на \n /panel")
    get_user(message)

@bot.message_handler(commands=['panel'])
def button_message(message : types.Message):
    Panel.get(message)

@bot.message_handler(commands=['game'])
def button_message(message : types.Message):
    Panel.Game(message)

def get_user(message : types.Message):
    print('id пользователя', message.chat.id)
    print('имя пользователя', message.from_user.first_name)
    print('фамилия пользователя', message.from_user.last_name)
    print('никнейм пользователя', message.from_user.username)    
    write_log(message)

@bot.message_handler(commands=['stop'])
def stop(message : types.Message):
    if(IsHost(message.chat.id)):
        bot.send_message(message.chat.id, 'Спокойной ночи', reply_markup=types.ReplyKeyboardRemove())
        write_log(message)
        bot.stop_bot()
        conn.close()
    else:
        bot.send_message(message.chat.id, 'Пошёл на хуй!\nТы не создатель.', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(content_types='text')
def message_reply(message : types.Message):
    write_log(message)
    if message.text=="Авторизация":
        user.Registration(message)
    elif message.text=="Новая игра":
        user.NewGame(message)
    elif message.text=="Сделать ход":
        user.Step(message)
    elif message.text=="Посмотреть поле":    
        bot.send_message(message.chat.id,'Где поле?')
        user.draw(message)
    elif message.text=="Завершить игру":    
        user.EndGame(message)
    else:
        bot.send_message(message.chat.id,f"{message.text}",reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, f"Для взаимодействия с ботом /panel \nДля игры /game\nДля админа /admin", reply_markup=types.ReplyKeyboardRemove())

print("Бот встал")

bot.infinity_polling()