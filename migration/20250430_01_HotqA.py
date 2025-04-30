"""

"""

from yoyo import step

__depends__ = {}

steps = [
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
        Сross       BIGINT          REFERENCES users(chat_id) ON DELETE CASCADE
    );
'''),
step("""
    CREATE TABLE field (
        x integer NOT NULL CHECK (x BETWEEN 1 AND 19),
        y integer NOT NULL CHECK (y BETWEEN 1 AND 19),
        user_id BIGINT REFERENCES users(chat_id) ON DELETE CASCADE,
        game_id integer REFERENCES game(id) ON DELETE CASCADE,
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
''')
]
