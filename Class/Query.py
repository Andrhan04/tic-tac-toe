import psycopg2
from configurate.Logs import write_exeption

conn = psycopg2.connect(dbname = "tic-tac-toe-19",
                        user="postgres",
                        password="pass",
                        host="127.0.0.1",
                        port="5432")

def Find(chat_id : int):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE chat_id = {chat_id}")
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    return (len(result) != 0 and len(result[0]) != 0)

def IsHost(chat_id : int):
    cursor = conn.cursor()
    cursor.execute(f'SELECT IsHost FROM Users WHERE chat_id = {chat_id}')
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    if(len(result) != 0 and len(result[0]) != 0 and result[0][0] != None):
        return result[0][0]
    else:
        return False

def Get_Users():
    cursor = conn.cursor()
    cursor.execute(f'SELECT chat_id, username, name FROM Users')
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    if(len(result) != 0 and len(result[0]) != 0):
        return result
    else:
        return False

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
        if(GetGame(chat_id_cross) == -1 and GetGame(chat_id_zero) == -1):
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO Game (Crosses, Zero) VALUES ({chat_id_cross},{chat_id_zero})")
            conn.commit()
            cursor.close()
        else:
            write_exeption("One is player was in game", "Query.CreateNewGame")
            raise Exception("One is player was in game")
    except Exception as e:
        write_exeption(str(e), "Query.CreateNewGame")

def GetGame(chat_id : int):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM game WHERE (Crosses = {chat_id} OR Zero = {chat_id}) AND NOT isend;")
        conn.commit()
        result = cursor.fetchall()
        cursor.close()
        if (len(result) == 0 or len(result[0]) == 0):
            return -1
        else:
            return result[0][0]
    except Exception as e:
        conn.rollback()
        cursor.close()
        write_exeption(str(e), "Query.GetGame")
        raise Exception("Can't get id on game")

def Step(chat_id : int, x: int, y:int):
    try:
        game_id = GetGame(chat_id)
    except Exception as e:
        write_exeption(str(e), "Query.Step")
        return 
    try:
        if(game_id == -1):
            write_exeption("No game", "Query.Step")
            raise Exception("No game")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO field (x, y, user_id, game_id) VALUES ({x}, {y}, {chat_id}, {game_id})")
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        write_exeption(str(e), "Query.Step")
        
def EndGame(game_id : int):
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE game SET IsEnd = true WHERE id = {game_id}")
        cursor.close()
        conn.commit()
    except Exception as e:
        conn.rollback()
        cursor.close()
        write_exeption(str(e), "Query.EndGame")
        raise Exception("Game not end")
        
def GetPrevStep(chat_id : int):
    try:
        game_id = GetGame(chat_id)
        if(game_id == -1):
            write_exeption("No game", "Query.Step")
            raise Exception("No game")
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM field WHERE game_id = {game_id} ORDER BY time DESC LIMIT 1;")
        result = cursor.fetchall()
        conn.commit()
        if (len(result) == 0 or len(result[0]) == 0):
            result = GetZero(game_id)
        else:
            return result[0][0]
        cursor.close()
    except Exception as e:
        conn.rollback()
        cursor.close()
        write_exeption(str(e), "Query.GetPrevStep")
        
def GetZero(game_id : int):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT Zero FROM game WHERE id = {game_id};")
        conn.commit()
        result = cursor.fetchall()
        cursor.close()
        if (len(result) == 0 or len(result[0]) == 0):
            raise Exception("No Game")
        else:
            return result[0][0]
    except Exception as e:
        conn.rollback()
        cursor.close()
        write_exeption(str(e), "Query.GetZero")
        
def GetCross(game_id : int):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT Crosses FROM game WHERE id = {game_id};")
        conn.commit()
        result = cursor.fetchall()
        cursor.close()
        if (len(result) == 0 or len(result[0]) == 0):
            raise Exception("No Game")
        else:
            return result[0][0]
    except Exception as e:
        conn.rollback()
        cursor.close()
        write_exeption(str(e), "Query.GetCross")
        
def GetMoves(game_id : int):
    "Получение ходов"
    try:
        cursor = conn.cursor()
        cursor.execute(f'''
                SELECT x, y, 
                CASE WHEN user_id = Zero
                    THEN false
                    ELSE true
                END my
                FROM field INNER JOIN game ON game_id = id
                WHERE game_id = {game_id}
            ''')
        res = cursor.fetchall()
        cursor.close()
        return res
    except Exception as e:
        conn.rollback()
        cursor.close()
        write_exeption(str(e), "Query.GetCross")