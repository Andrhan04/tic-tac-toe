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
        raise Exception("Can not create game")

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
        raise e
        
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
        cursor.close()
        if (len(result) == 0 or len(result[0]) == 0 or result[0][0] == None):
            result = GetZero(game_id)
            return result
        else:
            return result[0][0]
    except Exception as e:
        conn.rollback()
        cursor.close()
        write_exeption(str(e), "Query.GetPrevStep")
        raise Exception("Cant get user previos")
        
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

def isWin(chat_id : int):
    cursor = conn.cursor()
    game_id = GetGame(chat_id)
    cursor.execute(
        '''
            SELECT 
                x,
                y, 
                CASE WHEN user_id = Zero
                    THEN false
                    ELSE true
                END my
            FROM field INNER JOIN game ON game_id = id
            WHERE game_id = %s
            ORDER BY time DESC
        ''',
        (game_id,)
    )
    moves = cursor.fetchall()
    if(len(moves) == 361):
        return True
    if(len(moves) == 0):
        return False
    
    x = moves[0][0] - 1
    y = moves[0][1] - 1
    z = moves[0][2]
    symbol = ''
    if(z==False):
        symbol = 'O'
    else:
        symbol = 'X'
    directions = [
            [(0, 1), (0, -1)],  
            [(1, 0), (-1, 0)],  
            [(1, 1), (-1, -1)], 
            [(1, -1), (-1, 1)]   
        ]
    table = [''] * 19
    for i in range(19):
        table[i] = [''] * 19
    for row in moves: # Красим занятые
        if(row[2] == False):
            table[row[1] - 1][row[0] - 1] = 'O'
        else: 
            table[row[1] - 1][row[0] - 1] = 'X'
    n = 19
    for direction_pair in directions:
        total = 1  # Текущий ход уже учитывается
        for dx, dy in direction_pair:
            nx, ny = x + dx, y + dy
            while 0 <= nx < n and 0 <= ny < n and table[ny][nx] == symbol:
                total += 1
                nx += dx
                ny += dy
        if total >= 5:
            return True
    #print(table)
    return False

def GetBestStep_Dodo(game_id : int, Cross : int):
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
        WITH neighbours AS(
            SELECT x, y
            FROM (	
                SELECT x + dx x, y + dy y
                FROM field, generate_series(-1,1) dx, generate_series(-1,1) dy
                WHERE game_id = {game_id}
                UNION
                SELECT 10,10
            )
            WHERE (x,y) not in (SELECT x, y FROM field WHERE game_id = {game_id}) 
            AND x BETWEEN 1 AND 19 
            AND y BETWEEN 1 AND 19
        ), filled AS(
            SELECT 
                xx x,
                yy y, 
                CASE 
                    WHEN user_id = {Cross} THEN 'X' 
                    WHEN not user_id = {Cross} THEN 'O'
                    ELSE '.'
                END pos
            FROM generate_series(1,19) xx CROSS JOIN
            generate_series(1,19) yy LEFT JOIN field ON xx = x AND yy = y AND game_id = {game_id}
        ), lines AS(
            SELECT 1 x, y, 1 dx, 0 dy, string_agg(pos, ''ORDER BY x) line
            FROM filled GROUP BY y
            UNION
            SELECT x, 1, 0, 1, string_agg(pos,'' ORDER BY y)
            FROM filled GROUP BY x
            UNION
            SELECT 
                CASE WHEN x+y > 20 
                        THEN x+y-19 
                    ELSE 1
                END x,
                CASE WHEN x+y > 20 
                        THEN 19 
                    ELSE x+y-1
                END y,
                1, -1, string_agg(pos,'' ORDER BY x) line
            FROM filled GROUP BY x+y
            UNION
            SELECT 
                CASE WHEN x-y >=0 THEN x-y+1
                    ELSE 1
                END x,
                CASE WHEN x-y >=0 THEN 1
                    ELSE -(x-y) + 1
                END y,		
                1, 1, string_agg(pos,'' ORDER BY x) line
            FROM filled GROUP BY x-y
        ), new_move AS(
            SELECT n.x, n.y, delta, l.dx, l.dy, overlay(l.line PLACING '*' FROM delta+1) line
            FROM neighbours n CROSS JOIN generate_series(0,18) delta
            JOIN lines l ON n.x = l.x + l.dx * delta AND n.y = l.y + l.dy * delta  
        ), templates(weight, template) AS(
            VALUES
            (100000,  '*XXXX'), (100000,  'X*XXX'), (100000,  'XX*XX'),
            ( 31000,  '*OOOO'), ( 31000,  'O*OOO'), ( 31000,  'OO*OO'),
            ( 10000, '.*XXX.'), ( 10000, '.X*XX.'), ( 10000, '.X.*XX.'), ( 10000, '.X*.XX.'),
            (  3100, '.*OOO.'), (  3100, '.O*OO.'),
            (  1000, '.*XXXO'), (  1000, '.X*XXO'), (  1000, '.XX*XO'), (  1000, '.XXX*O'),
            (   310, '.*OOOX'), (   310, '.O*OOX'), (   310, '.OO*OX'), (   310, '.OOO*X'),
            (   800, '.*XX.'),  (   800, '.X*X.'),
            (   250, '.*OO.'),  (   250, '.O*O.'),
            (   500, '.*XXO'),  (   500, '.X*XO'),  (   500, '.XX*O'),
            (   150, '.*OOX'),  (   150, '.O*OX'),  (   150, '.OO*X'),
            (   100, '.*X.'),
            (    31, '.*O.'),
            (    10, '.*OX'),   (    10, '.O*X'),
            (     5, '.*.'),
            (     2, '.*O')
        ), templates_rev(weight,template) AS (
        SELECT weight, template FROM templates
        UNION
        SELECT weight, reverse(template) FROM templates
        ), sm_to_center AS(
            SELECT x, y, LEAST(x,y) sm
            FROM generate_series(1,10) x, generate_series(1,10) y
        ), all_sm_to_center AS(
            SELECT DISTINCT x, y, sm
            FROM (
                SELECT x, y, sm
                FROM sm_to_center
                UNION ALL
                SELECT 20 - x, y, sm
                FROM sm_to_center
                UNION ALL
                SELECT x, 20 - y, sm
                FROM sm_to_center
                UNION ALL
                SELECT 20 - x, 20 - y, sm
                FROM sm_to_center
            )
        ), costs(x,y,weight) AS(
            SELECT n.x, n.y, weight, sm
            FROM new_move n 
            JOIN templates_rev t ON n.line LIKE '%'||t.template||'%' JOIN all_sm_to_center a ON n.x = a.x AND n.y = a.y
            ORDER BY weight DESC, sm DESC
            LIMIT 1
        )
        SELECT x,y
        FROM costs;
        """)
        conn.commit()
        result = cursor.fetchall()
        cursor.close()
        return result[0]
    except Exception as e:
        conn.rollback()
        cursor.close()
        write_exeption(str(e),"Query.GetBestStep_Dodo")
        raise Exception("Can not Get Best Step")
    
def GetBestStep_IT(game_id : int, Cross : int):
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
        WITH neighbors(x,y) AS (
    -- ближайшие к занятым пустые клетки или центр пустого поля
    SELECT x, y 
    FROM (
        SELECT x+dx x, y+dy y 
        FROM field f, generate_series(-1,1) dx, generate_series(-1,1) dy  
        WHERE game_id = {game_id}
        UNION -- убираем дубликаты
        SELECT 10, 10
    )
    WHERE (x,y) NOT IN (SELECT x,y FROM field WHERE game_id = {game_id})
    AND x BETWEEN 1 AND 19
    AND y BETWEEN 1 AND 19
    ), filled(x,y,pos) AS (
    -- поле, дополненное пустыми клетками
    -- и представленное символами вместо boolean
    SELECT xx, yy, CASE WHEN user_id = {Cross} THEN 'X' WHEN NOT user_id = {Cross} THEN 'O' ELSE '.' END
    FROM generate_series(1,19) xx
        CROSS JOIN generate_series(1,19) yy
        LEFT JOIN field f ON f.x = xx AND f.y = yy AND game_id = {game_id}
    ), lines(x,y,dx,dy,line) AS (
    -- линии клеток:
    -- горизонтали
    SELECT 1, y, 1, 0, string_agg(pos,'' ORDER BY x) FROM filled GROUP BY y
    UNION ALL 
    -- вертикали
    SELECT x, 1, 0, 1, string_agg(pos,'' ORDER BY y) FROM filled GROUP BY x
    UNION ALL 
    -- диагонали
    SELECT CASE WHEN x+y > 20 THEN x+y-19 ELSE 1 END,
            CASE WHEN x+y > 20 THEN 19 ELSE x+y-1 END,
            1, -1, string_agg(pos,'' ORDER BY x) FROM filled GROUP BY x+y HAVING x+y BETWEEN 6 AND 34
    UNION ALL 
    SELECT CASE WHEN x-y >= 0 THEN 1+(x-y) ELSE 1 END,
            CASE WHEN x-y >= 0 THEN 1 ELSE 1-(x-y) END,
            1, 1, string_agg(pos,'' ORDER BY x) FROM filled GROUP BY x-y HAVING x-y BETWEEN -14 AND 14
    ), lines_per_move(x,y,delta,dx,dy,line) AS (
    -- линии в группировке по потенциальным ходам
    SELECT n.x, n.y, delta, l.dx, l.dy, overlay(l.line PLACING '*' FROM delta+1)
    FROM neighbors n
        CROSS JOIN generate_series(0,18) delta
        JOIN lines l ON n.x = l.x + l.dx*delta AND n.y = l.y + l.dy*delta
    ), templates(weight,template) AS (
    -- шаблоны с весами
    VALUES
        (100000,  '*XXXX'), (100000,  'X*XXX'), (100000,  'XX*XX'),
        ( 31000,  '*OOOO'), ( 31000,  'O*OOO'), ( 31000,  'OO*OO'),
        ( 10000, '.*XXX.'), ( 10000, '.X*XX.'),
        (  3100, '.*OOO.'), (  3100, '.O*OO.'),
        (  1000, '.*XXXO'), (  1000, '.X*XXO'), (  1000, '.XX*XO'), (  1000, '.XXX*O'),
        (   310, '.*OOOX'), (   310, '.O*OOX'), (   310, '.OO*OX'), (   310, '.OOO*X'),
        (   800, '.*XX.'),  (   800, '.X*X.'),
        (   250, '.*OO.'),  (   250, '.O*O.'),
        (   500, '.*XXO'),  (   500, '.X*XO'),  (   500, '.XX*O'),
        (   150, '.*OOX'),  (   150, '.O*OX'),  (   150, '.OO*X'),
        (   100, '.*X.'),
        (    31, '.*O.'),
        (    10, '.*OX'),   (    10, '.O*X'),
        (     5, '.*.'),
        (     2, '.*O')
    ), templates_rev(weight,template) AS (
    SELECT weight, template FROM templates
    UNION
    SELECT weight, reverse(template) FROM templates
    ), costs(x,y,weight) as (
    SELECT l.x, l.y, sum(t.weight)
    FROM lines_per_move l
        JOIN templates_rev t ON l.line LIKE '%'||t.template||'%'
    GROUP BY x, y
    )
    SELECT x, y FROM costs
    ORDER BY weight DESC, random()
    LIMIT 1;        """)
        conn.commit()
        result = cursor.fetchall()
        cursor.close()
        return result[0]
    except Exception as e:
        conn.rollback()
        cursor.close()
        write_exeption(str(e),"Query.GetBestStep_IT")
        raise Exception("Can not Get Best Step")
