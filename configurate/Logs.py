import json
from telebot import types
from datetime import date
from datetime import datetime
today = date. today()

def write_log(message : types.Message):
    Log = f"configurate\\log\\logs_{today}.txt"
    time = datetime.now().time()
    data : dict = {"chat_id":message.chat.id , "user_name" : message.from_user.username}
    data.update({ 'time' : str(time), 'message' : message.text})
    with open(Log, "a+", encoding='utf-8') as write_file:
        json.dump(data, write_file, ensure_ascii=False)
        write_file.write('\n')
        
def write_log_exeption(message : types.Message, text_exeption : str):
    Log = f"configurate\\log\\logs_{today}.txt"
    time = datetime.now().time()
    data : dict = {"chat_id":message.chat.id , "user_name" : message.from_user.username}
    data.update({ 'time' : str(time), 'exeption' : text_exeption, 'message': message.text})
    with open(Log, "a+", encoding='utf-8') as write_file:
        json.dump(data, write_file, ensure_ascii=False)
        write_file.write('\n')
        
def write_exeption(text_exeption : str, func : str):
    Log = f"configurate\\log\\logs_{today}.txt"
    time = datetime.now().time()
    data : dict = { 'time' : str(time), 'exeption' : text_exeption, "where" : func}
    with open(Log, "a+", encoding='utf-8') as write_file:
        json.dump(data, write_file, ensure_ascii=False)
        write_file.write('\n')