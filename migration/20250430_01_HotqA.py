"""

"""

from yoyo import step

__depends__ = {}

steps = [
step("""
    DROP TABLE IF EXISTS users, game, field;
"""),
step("""
    CREATE TABLE Users (
        chat_id     BIGINT      PRIMARY KEY,
        username    TEXT        NOT NULL CHECK (TRIM(username) = '' IS NOT TRUE),
        name        TEXT        NOT NULL CHECK (TRIM(name) = '' IS NOT TRUE),
        login_time  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP(0),
        IsHost      BOOLEAN     DEFAULT FALSE
    );
"""),
step('''
    CREATE TABLE Game(
        id          SERIAL          PRIMARY KEY,
        Times       TIMESTAMP       DEFAULT CURRENT_TIMESTAMP(0),
        IsEnd       BOOLEAN         DEFAULT FALSE,
        Zero        BIGINT          REFERENCES users(chat_id) ON DELETE CASCADE,
        Crosses     BIGINT          REFERENCES users(chat_id) ON DELETE CASCADE
    );
'''),
step("""
    CREATE TABLE field (
        x integer NOT NULL CHECK (x BETWEEN 1 AND 19),
        y integer NOT NULL CHECK (y BETWEEN 1 AND 19),
        user_id BIGINT REFERENCES users(chat_id) ON DELETE CASCADE,
        game_id integer REFERENCES game(id) ON DELETE CASCADE,
        time  TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0),
        UNIQUE (x, y, game_id)
    );
"""),
step('''
    DROP TRIGGER IF EXISTS name_trigger ON users;
    CREATE OR REPLACE FUNCTION name_validate()
    RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        NEW.name = REGEXP_REPLACE(LOWER(REGEXP_REPLACE(NEW.name,'[^[:alnum:][:space:]:/.-]+',' ','g')), '^[[:space:]]+|[[:space:]]+$|[[:space:]]+(?=[[:space:]])', '', 'g');
        NEW.name = INITCAP(TRIM(NEW.name));
        RETURN NEW;
    END;
    $$;
    CREATE TRIGGER name_trigger
    BEFORE INSERT OR UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION name_validate();
'''),
step("""
    INSERT INTO users (chat_id, username, name, IsHost) VALUES (5383313610, 'Han_Andr', 'Андрей', true);
    
    INSERT INTO users (chat_id, username, name, IsHost) VALUES (1058304013, 'Dodonyas', 'Доржи');
    
    INSERT INTO game (id, times, isend, Zero, Crosses) VALUES (1 ,2025-05-01 14:15:01, true,1058304013, 5383313610);
    
    INSERT INTO field (x,y,user_id,game_id,time) VALUES
        (9,	    9,	5383313610,	1,	    "2025-05-01 21:59:26"),
        (10,	10,	1058304013,	1,	    "2025-05-01 22:00:31"),
        (8,	    8,	5383313610,	1,	    "2025-05-01 22:00:48"),
        (11,	11,	1058304013,	1,	    "2025-05-01 22:01:38"),
        (10,	8,	5383313610,	1,	    "2025-05-01 22:02:05"),
        (7,	    11,	1058304013,	1,	    "2025-05-01 22:12:44"),
        (7,	    7,	5383313610,	1,	    "2025-05-01 22:13:50"),
        (9,	    11,	1058304013,	1,	    "2025-05-01 22:14:20"),
        (8,	    12,	5383313610,	1,	    "2025-05-01 22:15:20"),
        (6,	    6,	1058304013,	1,	    "2025-05-01 22:15:59"),
        (8,	    10,	5383313610,	1,	    "2025-05-01 22:16:52"),
        (7,	    12,	1058304013,	1,	    "2025-05-01 22:25:03"),
        (7,	    9,	5383313610,	1,	    "2025-05-01 22:30:34"),
        (8,	    11,	1058304013,	1,	    "2025-05-01 22:32:34"),
        (11,	9,	5383313610,	1,	    "2025-05-01 22:33:15"),
        (10,	11,	1058304013,	1,	    "2025-05-01 22:34:02");
        
    SELECT setval('game_id_seq', (SELECT max(id)+1 FROM game));
"""),
]
