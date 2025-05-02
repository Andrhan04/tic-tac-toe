from telebot import types
from Class.bot import bot
from configurate.Logs import write_log, write_log_exeption, write_exeption
import Class.Query as q
import matplotlib.pyplot as plt
import time
import matplotlib

matplotlib.use('agg')


#---------------------------------------------------------------------------------------------------------
# Регистрация
def Registration(message : types.Message):
    write_log(message)
    if(q.Find(int(message.chat.id))):
            bot.reply_to(message, 'Ты зарегестрирован', reply_markup=types.ReplyKeyboardRemove())
    else:
        msg = bot.reply_to(message, 'Твоё имя')
        bot.register_next_step_handler(msg, process_name_step)
        
def process_name_step(message : types.Message):
    write_log(message)
    try:
        if(message.from_user.username != None):
            username = message.from_user.username
        else:
            username = message.from_user.first_name
        q.Authorization(message.chat.id,username,message.text)
        bot.send_message(message.chat.id,"Авторизация пройдена")
    except Exception as e:
        write_log_exeption(message, str(e))
        bot.reply_to(message, 'Упс!')

#-----------------------------------------------------------------------------------------------------------------------------
# Новая игра

def NewGame(message : types.Message):
    game_id = q.GetGame(message.chat.id)
    if(game_id != -1):
        bot.send_message(message.chat.id, 'Ты в игре', reply_markup=types.ReplyKeyboardRemove())
        return
    write_log(message)
    if(q.Find(message.chat.id)): 
        arr_users = q.Get_Users()
        markup : types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for chat_id, username, name in arr_users:
            if(chat_id != message.chat.id):
                items : types.KeyboardButton = types.KeyboardButton(f"id = {chat_id} username = {username} name = {name}")
                markup.add(items)
        if(len(arr_users) == 1):
                bot.reply_to(message, 'Ты один', reply_markup=types.ReplyKeyboardRemove())
        else:
            msg = bot.send_message(message.chat.id, 'С кем поиграешь?', reply_markup=markup)
            bot.register_next_step_handler(msg, process_create_game)
    else:
        bot.reply_to(message, 'Пошёл на фиг не авторизованный!')
        
        
def process_create_game(message : types.Message):
    write_log(message)
    user_id = int(message.text.split()[2])
    try:
        q.CreateNewGame(message.chat.id, user_id)
        arr_users = q.Get_Users()
        Cross : str = ""
        Cross_name : str = ""
        for chat_id, username, name in arr_users:
                if(chat_id == message.chat.id):
                    Cross = username
                    Cross_name = name
        bot.send_message(user_id, f"Вас призвал в игру {Cross} с именем {Cross_name}", reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, f"Игра создана", reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        bot.send_message(message.chat.id, f"Пошёл на фиг", reply_markup=types.ReplyKeyboardRemove())
    
#----------------------------------------------------------------------------------------------------------------------------------
# Завершить игру

def EndGame(message : types.Message):
    write_log(message)
    try:
        game_id = q.GetGame(message.chat.id)
        if(game_id == -1):
            bot.send_message(message.chat.id, "Не было игры", reply_markup=types.ReplyKeyboardRemove())
        else:    
            try:
                q.EndGame(game_id)
            except Exception as e:
                write_log_exeption(message,str(e))
                bot.send_message(message.chat.id, "Игра продолжается!", reply_markup=types.ReplyKeyboardRemove())
                return
            Zero_id = q.GetZero(game_id)
            Cross_id = q.GetCross(game_id)
            bot.send_message(Zero_id, "Игра завершена", reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(Cross_id, "Игра завершена", reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        write_log_exeption(message,str(e))
        bot.send_message(message.chat.id, "Пиздец", reply_markup=types.ReplyKeyboardRemove())
        
#-----------------------------------------------------------------------------------------------------------------------------------
# Сделать ход

def Step(message : types.Message):
    write_log(message)
    try:
        game_id : int = q.GetGame(message.chat.id)
        if game_id == -1:
            bot.send_message(message.chat.id, "Ты не в игре", reply_markup=types.ReplyKeyboardRemove())
            return
        user_id : int = q.GetPrevStep(message.chat.id)
        if(user_id == message.chat.id):
            bot.send_message(message.chat.id, "Не твой ход", reply_markup=types.ReplyKeyboardRemove())
            return
    except Exception as e:
        write_log_exeption(message,str(e))
        bot.send_message(message.chat.id, "Не твой ход", reply_markup=types.ReplyKeyboardRemove())    
    try:
        bot.send_message(user_id, 'Противник делает ход', reply_markup=types.ReplyKeyboardRemove())
        msg = bot.send_message(message.chat.id, 'Куда сходить? \nНапиши два числа через пробел.', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_step)
    except Exception as e:
        write_log_exeption(message,str(e))
        bot.send_message(message.chat.id, "Пиздец", reply_markup=types.ReplyKeyboardRemove())
        
def process_step(message : types.Message):
    write_log(message)
    try:
        data = message.text.split()
        x = int(data[0])
        y = int(data[1])
        user_id : int = q.GetPrevStep(message.chat.id)
        try:
            q.Step(message.chat.id, x, y)
            draw(user_id)
            if(q.isWin(user_id)):
                EndGame(message)
            else:
                bot.send_message(user_id, "Твой ход", reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(message.chat.id, "Ход записан успешно", reply_markup=types.ReplyKeyboardRemove())
        except Exception as e:
            write_log_exeption(message,str(e))
            bot.send_message(message.chat.id, "Ты еблан?", reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        write_log_exeption(message,str(e))
        bot.send_message(message.chat.id, "Пиздец", reply_markup=types.ReplyKeyboardRemove())


#---------------------------------------------------------------------------------------------------------------------------------------------
path:str = "Images\\"

def ShowField(message : types.Message):
    "Отрисовка положения игры"
    draw(message.chat.id)

def draw(chat_id : int):
    "Отрисовка положения игры"
    game_id : int = q.GetGame(chat_id)
    if(game_id == -1):
        bot.send_message(chat_id, "Ты не в игре", reply_markup=types.ReplyKeyboardRemove())
        return
    try:
        moves = q.GetMoves(game_id) 
    except Exception as e:
        bot.send_message(chat_id, "Пиздец", reply_markup=types.ReplyKeyboardRemove())
        write_exeption(str(e),"USer.draw")
        raise e
    table = [''] * 19
    color = ['w'] * 19
    for i in range(19):
        table[i] = [''] * 19
        color[i] = ['w'] * 19
    
    for row in moves: # Красим занятые
        if(row[2] == False):
            table[row[1] - 1][row[0] - 1] = 'O'
            color[row[1] - 1][row[0] - 1] = 'b'
        else: 
            table[row[1] - 1][row[0] - 1] = 'X'
            color[row[1] - 1][row[0] - 1] = 'r'

    fig, ax = plt.subplots(1, 1, figsize=(7,7))
    column_labels = [i for i in range(1,20)]    
    ax.axis("tight") 
    tbl = ax.table(cellText = table, colLabels = column_labels, rowLabels = column_labels, loc="center", cellLoc='center', cellColours=color) 
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(14)  # Размер шрифта
    fig.supxlabel('X')
    fig.supylabel('Y')
    ax.set_aspect('equal')
    for (row, col), cell in tbl.get_celld().items():
        if row == 0:  # Заголовки столбцов
            cell.set_text_props(color='black', weight='bold')  
        else:  # Остальные ячейки
            if(col == -1):
                cell.set_text_props(color='black', weight='bold') 
            else: # Заголовки строк
                cell.set_text_props(color='white', weight='bold')
    ax.axis("off") 
    # plt.show()
    plt.savefig(path + f'table_{game_id}_{len(moves)}.png')
    plt.close(fig)
    #time.sleep(3)
    photo = open(path + f'table_{game_id}_{len(moves)}.png', 'rb')
    bot.send_photo(chat_id, photo)