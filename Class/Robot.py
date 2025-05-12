from telebot import types
from configurate.Logs import write_log, write_log_exeption, write_exeption
import Class.Query as q
import time as t

def Best_Step(message : types.Message, id : int):
    if(id == -1):
        Best_Step_Dodo()
    elif(id == -2):
        Best_Step_IT()
    else:
        raise Exception("No bot")


#---------------------------------------------------------------------------------------
# Dodo
def Best_Step_Dodo():
    try:
        t.sleep(1)
        game_id : int = q.GetGame(-1)
        x,y = q.GetBestStep_Dodo(game_id,-1)
        q.Step(-1, x, y)
    except Exception as e:
        raise Exception("Can not do step")



#---------------------------------------------------------------------------------------
# IT Planet

def Best_Step_IT():
    try:
        t.sleep(1)
        game_id : int = q.GetGame(-2)
        x,y = q.GetBestStep_IT(game_id,-2)
        q.Step(-2, x, y)
    except Exception as e:
        raise Exception("Can not do step")
    