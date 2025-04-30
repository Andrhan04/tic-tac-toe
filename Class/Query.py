import psycopg2
from configurate.Logs import write_exeption

conn = psycopg2.connect(dbname = "tic-tac-toe-19",
                        user="postgres",
                        password="pass",
                        host="127.0.0.1",
                        port="5432")

def Authorization(chat_id : int, username : str, name : str):
    try:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Users (chat_id,username,name) VALUES ({chat_id},'{username}','{name}')")
        conn.commit()
        cursor.close()
    except Exception as e:
        write_exeption(str(e), "Query.Authorization")

def CreateNewGame(chat_id_cross : int, chat_id_zero : int):
    try:
        if(GetGame(chat_id_cross) != -1 or GetGame(chat_id_zero) != -1):
            write_exeption("One is player was in game", "Query.CreateNewGame")
            raise Exception("One is player was in game")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Game (Сross, Zero) VALUES ({chat_id_cross},{chat_id_zero})")
        conn.commit()
        cursor.close()
    except Exception as e:
        write_exeption(str(e), "Query.CreateNewGame")

def GetGame(chat_id : int):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM game WHERE (Сross = {chat_id} OR Zero = {chat_id}) AND NOT isend")
        conn.commit()
        result = cursor.fetchall()
        cursor.close()
        if (len(result) == 0 or len(result[0]) == 0):
            return -1
        else:
            return result[0][0]
    except Exception as e:
        write_exeption(str(e), "Query.CreateNewGame")
        raise Exception("Can't get id on game")

def Step(chat_id : int, x: int, y:int):
    try:
        game_id = GetGame(chat_id)
        if(game_id == -1):
            write_exeption("No game", "Query.Step")
            raise Exception("No game")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO field (x, y, user_id, game_id) VALUES ({x},{y},{chat_id},{game_id})")
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        cursor.close()
        write_exeption(str(e), "Query.Step")
        
def EndGame(chat_id : int):
    try:
        game_id = GetGame(chat_id)
        if(game_id == -1):
            write_exeption("No game", "Query.Step")
            raise Exception("No game")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE game SET IsEnd = true WHERE id = {game_id}")
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        cursor.close()
        write_exeption(str(e), "Query.Step")
        